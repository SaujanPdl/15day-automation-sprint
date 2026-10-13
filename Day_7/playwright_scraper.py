import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_FILE = Path("Day_7/quotes_scraped.json")
TARGET_URL = "https://quotes.toscrape.com/js/"


def scrape_dynamic_quotes(max_pages=3):
    results = []

    # Deliverable 2: Launch headless Chromium and navigate to dynamic portals
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"[*] Navigating to {TARGET_URL} ...")
        page.goto(TARGET_URL)

        current_page = 1

        while current_page <= max_pages:
            print(f"\n[*] Processing Page {current_page}...")

            # Deliverable 4: Wait for JavaScript hydration to complete
            page.wait_for_selector(".quote")

            quote_elements = page.query_selector_all(".quote")
            print(f"[✓] Extracted {len(quote_elements)} quotes rendered by JavaScript.")

            for q in quote_elements:
                text_elem = q.query_selector(".text")
                author_elem = q.query_selector(".author")
                tag_elems = q.query_selector_all(".tag")

                quote_text = text_elem.inner_text().strip() if text_elem else ""
                author = author_elem.inner_text().strip() if author_elem else ""
                tags = [t.inner_text().strip() for t in tag_elems]

                results.append({
                    "quote": quote_text,
                    "author": author,
                    "tags": tags,
                    "page": current_page
                })

            # Deliverable 3: Handle pagination by checking and clicking 'Next'
            next_button = page.query_selector("li.next > a")

            if not next_button:
                print("[!] No 'Next' button detected. Reached final page.")
                break

            if current_page < max_pages:
                print("[*] Clicking 'Next' button to paginate...")
                next_button.click()
                # Wait for network or DOM transition
                page.wait_for_load_state("domcontentloaded")
                current_page += 1
            else:
                print(f"[✓] Reached requested limit of {max_pages} pages.")
                break

        browser.close()

    # Save extracted dataset
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Saved {len(results)} total records across {current_page} pages to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    scrape_dynamic_quotes(max_pages=3)