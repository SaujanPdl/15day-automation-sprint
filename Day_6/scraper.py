import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests

OUTPUT_JSON = Path("Day_6/scraped_books.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

TARGET_URL = "https://books.toscrape.com/catalogue/category/books_1/index.html"


def scrape_catalog():
  print("[*] Sending HTTP GET request with realistic headers...")
  response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
  response.raise_for_status()

  print(
      f"[✓] Response received: Status Code {response.status_code}. Parsing"
      " HTML..."
  )
  soup = BeautifulSoup(response.text, "html.parser")

  book_cards = soup.select("article.product_pod")
  print(f"[✓] Located {len(book_cards)} items using CSS selector.")

  scraped_records = []

  for card in book_cards:
  
    title_tag = card.find("h3").find("a")
    title = title_tag.get("title", title_tag.text)

   
    price_tag = card.find("p", class_="price_color")
    raw_price = price_tag.text if price_tag else "N/A"


    avail_tag = card.select_one("p.instock.availability")
    raw_availability = avail_tag.text if avail_tag else "Unknown"

    rating_tag = card.find("p", class_="star-rating")
    classes = rating_tag.get("class", []) if rating_tag else []
    rating = [c for c in classes if c != "star-rating"]
    rating_str = rating[0] if rating else "Not Rated"

    record = {
        "title": title.strip(),
        "price": raw_price.strip(),
        "availability": raw_availability.strip(),
        "rating": rating_str.strip(),
    }
    scraped_records.append(record)

  OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
  with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(scraped_records, f, indent=2, ensure_ascii=False)

  print(f"[✓] Successfully scraped {len(scraped_records)} items.")
  print(f"[✓] Saved records to {OUTPUT_JSON}")


  print("\n--- Preview Sample ---")
  for item in scraped_records[:3]:
    print(
        f"• {item['title'][:30]:<32} | {item['price']:<8} |"
        f" {item['availability']}"
    )


if __name__ == "__main__":
  scrape_catalog()