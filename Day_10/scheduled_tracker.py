import os
import re
import json
import time
import logging
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import schedule

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

HISTORY_FILE = Path("Day_10/price_history.json")
LOG_FILE = Path("Day_10/tracker.log")


LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  
    ]
)

TARGET_PRODUCTS = [
    {
        "id": "PROD-001",
        "title": "A Light in the Attic",
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    },
    {
        "id": "PROD-002",
        "title": "Tipping the Velvet",
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
    },
    {
        "id": "PROD-003",
        "title": "Soumission",
        "url": "https://books.toscrape.com/catalogue/soumission_998/index.html"
    },
    {
        "id": "PROD-004",
        "title": "Sharp Objects",
        "url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    }
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def load_price_history():
    if not HISTORY_FILE.exists():
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Failed to read price history: {e}")
        return {}


def save_price_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def fetch_current_price(url: str) -> float:
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    price_elem = soup.select_one("p.price_color")
    if not price_elem:
        raise ValueError("Price element not found")

    match = re.search(r"([0-9]+\.[0-9]+)", price_elem.get_text().strip())
    if match:
        return float(match.group(1))
    raise ValueError("Could not parse numeric price string")


def dispatch_discord_alert(title: str, url: str, old_price: float, new_price: float):
    if not WEBHOOK_URL:
        logging.warning("No DISCORD_WEBHOOK_URL set. Skipping webhook alert.")
        return

    savings_pct = ((old_price - new_price) / old_price) * 100

    payload = {
        "username": "Price Sentinel Engine",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "embeds": [
            {
                "title": f"🚨 Price Drop Triggered: {title}",
                "url": url,
                "color": 3066993,
                "fields": [
                    {"name": "Historical Min", "value": f"£{old_price:,.2f}", "inline": True},
                    {"name": "New Low Price", "value": f"**£{new_price:,.2f}**", "inline": True},
                    {"name": "Savings", "value": f"**{savings_pct:.1f}% OFF**", "inline": True},
                    {"name": "Listing URL", "value": f"[Open Product Listing]({url})", "inline": False}
                ],
                "footer": {"text": "Scheduled Price Tracker Engine • Day 10"},
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }

    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code == 204:
            logging.info(f"Webhook alert successfully delivered for: {title}")
        else:
            logging.error(f"Webhook delivery failed: HTTP {resp.status_code}")
    except Exception as exc:
        logging.error(f"Error dispatching webhook: {exc}")


def check_prices_job():
    """Scheduled job execution cycle."""
    logging.info("Starting scheduled pricing audit cycle...")
    history = load_price_history()
    now_iso = datetime.utcnow().isoformat()
    alerts_fired = 0

    for item in TARGET_PRODUCTS:
        p_id = item["id"]
        title = item["title"]
        url = item["url"]

        try:
            current_price = fetch_current_price(url)
            logging.info(f"Scraped '{title}' -> Current: £{current_price:.2f}")
        except Exception as e:
            logging.error(f"Failed scraping '{title}': {e}")
            continue

        if p_id not in history:
            history[p_id] = {
                "title": title,
                "url": url,
                "baseline_price": current_price,
                "historical_min": current_price,
                "history": []
            }
            logging.info(f"Initialized baseline for '{title}' at £{current_price:.2f}")

        record = history[p_id]
        historical_min = record.get("historical_min", current_price)
        threshold = historical_min * 0.95

        # Check drop threshold
        if current_price < threshold:
            logging.info(f"Price alert condition met for '{title}' (Current: £{current_price:.2f} < Threshold: £{threshold:.2f})")
            dispatch_discord_alert(title, url, historical_min, current_price)
            alerts_fired += 1
            record["historical_min"] = current_price
        elif current_price < historical_min:
            record["historical_min"] = current_price

        record["history"].append({
            "timestamp": now_iso,
            "price": current_price
        })

    save_price_history(history)
    logging.info(f"Audit cycle complete. Alerts dispatched: {alerts_fired}\n")


def start_scheduler():

    logging.info("Initializing background scheduler service...")
    
    # Run immediately once on launch
    check_prices_job()

    schedule.every(10).minutes.do(check_prices_job)

    logging.info("Scheduler active. Waiting for next interval (Press Ctrl+C to stop)...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")


if __name__ == "__main__":
    start_scheduler()