from pathlib import Path
import time
import pandas as pd


BRANCH_DIR = Path("Day_5/branches")
OUTPUT_FILE = Path("Day_5/master_reconciliation_report.xlsx")


def print_banner():
  print("=" * 60)
  print("   MULTI-BRANCH SALES RECONCILER ENGINE (v1.0)")
  print("   Automated Ingestion, Data Auditing & Master Reporting")
  print("=" * 60)


def generate_mock_branches():
  """Generates 3 test branch spreadsheets with intentional flaws."""
  BRANCH_DIR.mkdir(parents=True, exist_ok=True)

  data_a = {
      "Invoice_ID": ["INV-101", "INV-102", "INV-103", "INV-104"],
      "Client_Name": ["Apex Ltd", "Himalayan Tech", None, "Valley Store"],
      "Amount": [45000, 78000, 32000, 15000],
      "Date": ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"],
  }

  data_b = {
      "Invoice_ID": ["INV-201", "INV-102", "INV-203", "INV-204"],
      "Client_Name": ["Lakeside Cafe", "Himalayan Tech", "Fishtail Media", ""],
      "Amount": [22000, 78000, 64000, 11000],
      "Date": ["2026-09-01", "2026-09-03", "2026-09-04", "2026-09-05"],
  }

  data_c = {
      "Invoice_ID": ["INV-301", "INV-104", "INV-303", "INV-304"],
      "Client_Name": [
          "Patan Handicrafts",
          "Valley Store",
          "Durbar IT",
          "Sajha Mart",
      ],
      "Amount": [53000, 15000, 92000, 41000],
      "Date": ["2026-09-02", "2026-09-03", "2026-09-05", "2026-09-06"],
  }

  pd.DataFrame(data_a).to_excel(
      BRANCH_DIR / "branch_kathmandu.xlsx", index=False
  )
  pd.DataFrame(data_b).to_excel(BRANCH_DIR / "branch_pokhara.xlsx", index=False)
  pd.DataFrame(data_c).to_excel(BRANCH_DIR / "branch_lalitpur.xlsx", index=False)


def run_pipeline():
  print_banner()
  start_time = time.time()

  # Step 1: Scan directory
  print(f"[*] Scanning directory: '{BRANCH_DIR}' ...")
  excel_files = list(BRANCH_DIR.glob("*.xlsx"))

  if not excel_files:
    print("[!] No files found. Generating sample branch workbooks...")
    generate_mock_branches()
    excel_files = list(BRANCH_DIR.glob("*.xlsx"))

  print(f"[✓] Found {len(excel_files)} branch workbooks to ingest.\n")

  # Step 2: Batch read & ingest
  frames = []
  for file_path in excel_files:
    branch_name = file_path.stem.replace("branch_", "").capitalize()
    print(f"  -> Parsing {file_path.name:<24} | Tag: [{branch_name}]")
    df = pd.read_excel(file_path)
    df["Source_Branch"] = branch_name
    frames.append(df)

  combined_df = pd.concat(frames, ignore_index=True)
  print(f"\n[✓] Ingestion complete: {len(combined_df)} total records loaded.")

  # Step 3: Audit checks
  print("[*] Running automated integrity audit...")
  combined_df["Client_Name"] = combined_df["Client_Name"].replace(
      r"^\s*$", None, regex=True
  )

  duplicate_mask = combined_df.duplicated(subset=["Invoice_ID"], keep=False)
  missing_client_mask = combined_df["Client_Name"].isna()

  flagged_rows = []
  for idx, row in combined_df.iterrows():
    reasons = []
    if duplicate_mask[idx]:
      reasons.append("Duplicate Invoice ID")
    if missing_client_mask[idx]:
      reasons.append("Missing Client Name")

    if reasons:
      row_dict = row.to_dict()
      row_dict["Audit_Reason"] = " | ".join(reasons)
      flagged_rows.append(row_dict)

  audit_df = pd.DataFrame(flagged_rows)
  print(
      f"  -> Duplicates detected : {duplicate_mask.sum()} instances across"
      " branches"
  )
  print(f"  -> Missing client entries: {missing_client_mask.sum()} records")
  print(f"[!] Total flagged anomalies: {len(audit_df)}")

  # Step 4: Aggregate KPIs
  summary_metrics = (
      combined_df.groupby("Source_Branch")
      .agg(
          Total_Transactions=("Invoice_ID", "count"),
          Total_Revenue=("Amount", "sum"),
          Avg_Ticket_Size=("Amount", "mean"),
      )
      .reset_index()
  )

  # Step 5: Export multi-sheet workbook
  print(f"\n[*] Compiling multi-sheet master report to '{OUTPUT_FILE}'...")
  with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    summary_metrics.to_excel(writer, sheet_name="Summary", index=False)
    combined_df.to_excel(writer, sheet_name="Consolidated_Sales", index=False)
    if not audit_df.empty:
      audit_df.to_excel(writer, sheet_name="Audit_Flags", index=False)
    else:
      pd.DataFrame({"Status": ["All records passed audit"]}).to_excel(
          writer, sheet_name="Audit_Flags", index=False
      )

  elapsed = time.time() - start_time
  print(f"[✓] Done in {elapsed:.2f}s! Master report ready for executive review.")
  print("=" * 60)


if __name__ == "__main__":
  run_pipeline()