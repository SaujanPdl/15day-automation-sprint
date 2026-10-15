import os
import re
import json
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load webhook URL from root .env
load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

HISTORY_FILE = Path("Day_9/price_history.json")

# Deliverable 1: 3-5 real target products (using books.toscrape sandbox for reliable tests)
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
    """Deliverable 2: Load or initialize the local price history database."""
    if not HISTORY_FILE.exists():
        # Seed an initial baseline if file does not exist
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_price_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def fetch_current_price(url: str) -> float:
    """Scrapes the live product page and extracts price as a float."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    price_elem = soup.select_one("p.price_color")
    if not price_elem:
        raise ValueError(f"Could not locate price element on {url}")

    # Remove currency symbols (e.g. £51.77 -> 51.77)
    raw_str = price_elem.get_text().strip()
    match = re.search(r"([0-9]+\.[0-9]+)", raw_str)
    if match:
        return float(match.group(1))
    raise ValueError(f"Failed to parse price float from: {raw_str}")


def dispatch_discord_alert(title: str, url: str, old_price: float, new_price: float):
    """Sends price-drop embed notification via Discord Webhook."""
    if not WEBHOOK_URL:
        print(f"    [!] DISCORD_WEBHOOK_URL not configured. Skipping push alert.")
        return

    drop_percent = ((old_price - new_price) / old_price) * 100

    payload = {
        "username": "Price Sentinel Engine",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "embeds": [
            {
                "title": f"🔥 Price Drop Triggered: {title}",
                "url": url,
                "color": 3066993,  # Green
                "fields": [
                    {"name": "Previous Benchmark", "value": f"£{old_price:,.2f}", "inline": True},
                    {"name": "New Low Price", "value": f"**£{new_price:,.2f}**", "inline": True},
                    {"name": "Discount", "value": f"**{drop_percent:.1f}% OFF**", "inline": True},
                    {"name": "Listing URL", "value": f"[Open Product Listing]({url})", "inline": False}
                ],
                "footer": {"text": "Day 9 Deal Tracker Engine"},
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if r.status_code == 204:
            print("    [✓] Discord webhook notification sent!")
        else:
            print(f"    [-] Discord failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"    [-] Webhook exception: {e}")


def run_price_tracker():
    print("=" * 60)
    print("   COMPETITOR PRICE & DEAL TRACKER ENGINE (DAY 9)")
    print("=" * 60)

    history = load_price_history()
    now_iso = datetime.utcnow().isoformat()
    total_alerts = 0

    for item in TARGET_PRODUCTS:
        p_id = item["id"]
        title = item["title"]
        url = item["url"]

        print(f"\n[*] Checking: {title} ({p_id})...")
        try:
            current_price = fetch_current_price(url)
            print(f"    Current Live Price: £{current_price:.2f}")
        except Exception as e:
            print(f"    [!] Error scraping {title}: {e}")
            continue

        # Initialize product entry in history if not present
        if p_id not in history:
            # Deliverable 2: Store baseline benchmark prices
            history[p_id] = {
                "title": title,
                "url": url,
                "baseline_price": current_price,
                "historical_min": current_price,
                "history": []
            }
            print(f"    [+] Initialized baseline benchmark: £{current_price:.2f}")

        record = history[p_id]
        historical_min = record.get("historical_min", current_price)

        # Deliverable 3: Price comparison logic: current_price < historical_min * 0.95
        alert_threshold = historical_min * 0.95

        if current_price < alert_threshold:
            print(f"    [🚨 ALERT] Price dropped below 95% of historical low (£{historical_min:.2f})!")
            dispatch_discord_alert(title, url, historical_min, current_price)
            total_alerts += 1
            # Update record historical minimum
            record["historical_min"] = current_price
        else:
            print(f"    [-] No discount threshold met (Need < £{alert_threshold:.2f}, got £{current_price:.2f})")

        # Keep minimum updated if lower
        if current_price < record["historical_min"]:
            record["historical_min"] = current_price

        # Deliverable 4: Append every scraping run timestamp to maintain an audit history
        record["history"].append({
            "timestamp": now_iso,
            "price": current_price
        })

    save_price_history(history)
    print("\n" + "=" * 60)
    print(f"[✓] Run finished. Updated '{HISTORY_FILE}'.")
    print(f"[✓] Alerts triggered this run: {total_alerts}")
    print("=" * 60)


if __name__ == "__main__":
    run_price_tracker()