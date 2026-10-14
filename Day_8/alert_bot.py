import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load secrets from .env
load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_alert(
    title: str,
    deal_url: str,
    original_price: float,
    current_price: float,
    currency: str = "NPR",
) -> bool:
  """Dispatches a rich embed deal notification to a Discord webhook."""
  if not WEBHOOK_URL:
    print(
        "[-] Error: DISCORD_WEBHOOK_URL is not set in environment or .env"
        " file."
    )
    return False

  # Calculate savings percentage
  savings_pct = (
      ((original_price - current_price) / original_price) * 100
      if original_price > 0
      else 0.0
  )

  # Color: Green (0x2ECC71 -> 3066993) for solid deals, Red (0xE74C3C) if price increase
  embed_color = 3066993 if savings_pct > 0 else 15158332

  # Deliverables 2 & 3: Rich embed payload structure
  payload = {
      "username": "Deal Tracker Sentinel",
      "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
      "embeds": [{
          "title": f"🚨 Price Drop Detected: {title}",
          "url": deal_url,
          "description": (
              "A monitored item just dropped below its historical average."
          ),
          "color": embed_color,
          "fields": [
              {
                  "name": "Current Price",
                  "value": f"**{currency} {current_price:,.2f}**",
                  "inline": True,
              },
              {
                  "name": "Original Price",
                  "value": f"~~{currency} {original_price:,.2f}~~",
                  "inline": True,
              },
              {
                  "name": "Savings",
                  "value": f"**{savings_pct:.1f}% OFF**",
                  "inline": True,
              },
              {
                  "name": "Direct Purchase Link",
                  "value": f"[View on Store]({deal_url})",
                  "inline": False,
              },
          ],
          "footer": {
              "text": "Automated Alert Engine • 15-Day Automation Sprint",
              "icon_url": (
                  "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
              ),
          },
          "timestamp": datetime.utcnow().isoformat(),
      }],
  }

  print(f"[*] Dispatching webhook payload for '{title}'...")
  response = requests.post(WEBHOOK_URL, json=payload, timeout=10)

  if response.status_code == 204:
    print("[✓] Notification delivered successfully to Discord.")
    return True
  else:
    print(f"[-] Delivery failed with status {response.status_code}:")
    print(f"    {response.text}")
    return False


if __name__ == "__main__":
  # Sample live run: Price alert trigger demo
  test_deal = {
      "title": "Logitech MX Master 3S Wireless Performance Mouse",
      "deal_url": (
          "https://www.logitech.com/en-us/products/mice/mx-master-3s.html"
      ),
      "original_price": 14500.0,
      "current_price": 10875.0,
      "currency": "NPR",
  }

  send_discord_alert(**test_deal)