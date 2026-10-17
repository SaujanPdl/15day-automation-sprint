# ⚡ 15-Day Python Automation & Scripting Sprint

A collection of lightweight Python automation scripts, data wrangling pipelines (Pandas), and practical tools built during an intensive 15-day sprint.

---

## 📁 Daily Builds

### Day 1: Automated File & Directory Sorter (`Day_1/`)
* **Problem Solved:** Automatically organizes cluttered folders (Downloads, Desktop) by extension.
* **Tech Used:** `pathlib`, `shutil`
* **Features:**
  * Groups files dynamically into extension-based directories (PDF, CSV, PNG, etc.).
  * Defensive checks for duplicate files to prevent overwriting.
  * Handles locked/in-use files gracefully with `try/except`.

---

### Day 2: Sales Data Cleaning & Financial Reconciliation (`Day_2/`)
* **Problem Solved:** Cleans messy transaction exports and generates multi-tab executive financial summaries in seconds.
* **Tech Used:** `pandas`, `openpyxl`, `pathlib`
* **Features:**
  * Trims whitespace and normalizes branch/item names.
  * Resolves inconsistent date formats and drops corrupted values.
  * Filters out invalid quantities (zero/negative records).
  * Automatically calculates 13% VAT, gross, and net revenue.
  * Exports clean raw data along with branch and product summary sheets into an Excel workbook (`.xlsx`).

---

### Day 3: OpenPyXL Excel Formatting & Executive Styling (`Day_3/`)
* **Problem Solved:** Transforms raw, unformatted Excel exports into executive-ready financial reports with custom styling and formatting.
* **Tech Used:** `openpyxl`, `os`
* **Features:**
  * Ingests existing workbooks dynamically with `load_workbook()`.
  * Applies executive styling with solid navy headers, bold white typography, and clean grid borders.
  * Formats financial columns into standard currency representation (`NPR #,##0.00`).
  * Calculates maximum string lengths across rows and dynamically auto-fits column widths to prevent truncation (`###`).

---

### Day 4: Demo 1 - Multi-Branch Sales Reconciler Engine (`Day_4/`)
* **Problem Solved:** Automates batch ingestion of regional branch sales workbooks, detects duplicate cross-branch invoices, flags missing entries, and generates an audited executive summary.
* **Tech Used:** `pandas`, `openpyxl`, `pathlib`
* **Features:**
  * Uses `pathlib` globbing to dynamically batch-read every branch `.xlsx` workbook from a dedicated folder.
  * Consolidates disparate branch datasets into a unified DataFrame using `pd.concat()` while stamping source origin.
  * Audits records for data hygiene by flagging cross-branch duplicate invoice IDs and null/empty client values.
  * Exports an executive multi-sheet master workbook containing high-level `Summary` metrics, `Consolidated_Sales`, and an itemized `Audit_Flags` sheet.


---

### Day 5: Demo 1 Polish - Sales Reconciler Engine & Executive Package (`Day_5/`)
* **Problem Solved:** Manually consolidating multi-branch reports takes hours every week while missing duplicate invoice IDs and silent data entry omissions.
* **Tech Used:** `pandas`, `openpyxl`, `pathlib`, `time`
* **Features:**
  * Terminal CLI runner with execution tracking, anomaly counts, and timing benchmarks.
  * Automated batch ingestion across regional branch spreadsheets with origin tracking.
  * Cross-branch data auditing that isolates duplicate invoice numbers and missing client records.
  * Exports an executive multi-sheet workbook containing `Summary` KPIs, `Consolidated_Sales`, and an isolated `Audit_Flags` tab.

---

### Day 6: HTTP Requests & BeautifulSoup Web Scraping (`Day_6/`)
* **Problem Solved:** Manually gathering catalog prices and inventory data across web listings is slow, error-prone, and unscalable.
* **Tech Used:** `requests`, `beautifulsoup4`, `json`
* **Features:**
  * Configures realistic browser `User-Agent` headers to prevent request blocking.
  * Navigates the HTML tree using both standard element methods (`.find()`, `.find_all()`) and CSS selectors (`.select()`).
  * Cleans extracted strings by trimming newlines and whitespace using `.strip()`.
  * Exports sanitized structured records into a formatted JSON dataset.

---

### Day 7: Headless Browser Scraping with Playwright (`Day_7/`)
* **Problem Solved:** Standard HTTP requests fail on modern Single Page Applications (SPAs) where data is injected dynamically via client-side JavaScript.
* **Tech Used:** `playwright`, `json`, `pathlib`
* **Features:**
  * Automates headless Chromium execution to parse client-hydrated DOM structures.
  * Uses explicit element waiting (`wait_for_selector`) to handle asynchronous DOM updates without race conditions.
  * Handles interactive multi-page pagination by detecting and clicking dynamic "Next" navigational controls.
  * Extracts structured records into a clean, normalized JSON format.


---

### Day 8: Automated Discord Webhook Alert Bot (`Day_8/`)
* **Problem Solved:** Scraping engines and background jobs require instant notification systems so users don't need to manually monitor terminal outputs or poll databases.
* **Tech Used:** `requests`, `python-dotenv`, `datetime`
* **Features:**
  * Dispatches structured Discord webhook payloads using RESTful HTTP POST requests.
  * Dynamically computes pricing variance and savings percentages for triggered products.
  * Formats rich embed cards featuring real-time timestamps, inline KPI fields, discount indicators, and direct store URLs.
  * Secures sensitive webhook credentials using external `.env` configuration.

---

### Day 9: Demo 2 - Competitor Price & Deal Tracker Engine (`Day_9/`)
* **Problem Solved:** E-commerce stores and consumers lose money by failing to track fluctuating competitor prices and missing short-lived discount opportunities.
* **Tech Used:** `requests`, `beautifulsoup4`, `python-dotenv`, `json`
* **Features:**
  * Monitors target product listings dynamically with automated DOM traversal and regex price sanitization.
  * Persists historical pricing data and baseline benchmarks inside a structured `price_history.json` database.
  * Implements automated anomaly comparison logic triggering deal alerts when `current_price < historical_min * 0.95`.
  * Logs ISO timestamps on every run to build a continuous pricing audit trail.
  * Dispatches rich Discord webhook embeds when significant discounts are detected.


---

### Day 10: Demo 2 Release - Task Scheduling & Automated Auditing (`Day_10/`)
* **Problem Solved:** Price tracking scripts fail to provide value if they require manual terminal execution and lack persistent runtime diagnostic logs.
* **Tech Used:** `schedule`, `logging`, `requests`, `beautifulsoup4`, `python-dotenv`, `json`
* **Features:**
  * Configures an automated task scheduler using Python's declarative `schedule` module for hands-free background execution.
  * Replaces console prints with production-grade file logging (`tracker.log`) tracking process timestamps, network responses, and alerts.
  * Implements dynamic anomaly detection triggering instant Discord webhook alerts upon detecting a $\ge 5\%$ drop from historical lows.
  * Maintains a JSON audit history appending time-series pricing data for every scrape interval.

---

### Day 11: Standalone Windows Executable Packaging (`Day_11/`)
* **Problem Solved:** Non-technical corporate clients cannot run command-line tools or install Python runtimes and dependencies.
* **Tech Used:** `pyinstaller`, `tkinter`, `pandas`, `openpyxl`, `pathlib`
* **Features:**
  * Packages automation pipelines into an isolated, single-file Windows executable (`.exe`) via PyInstaller.
  * Resolves internal temp assets and bundled configurations using `sys._MEIPASS` dynamic path resolution.
  * Suppresses the terminal console (`--windowed`) in favor of native OS dialog boxes for a seamless end-user experience.
  * Operates fully standalone on clean client machines without requiring pre-installed Python interpreters or virtual environments.