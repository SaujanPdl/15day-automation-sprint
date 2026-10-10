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
  