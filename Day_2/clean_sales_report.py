from pathlib import Path
import pandas as pd

csv_file = Path("data/raw_sales.csv")

if not csv_file.exists():
    csv_file.parent.mkdir(exist_ok=True)
    dummy_data = {
        "txn_id": [101, 102, 103, 104, 105],
        "date": ["2026-09-20", "2026/09/21", "bad_date", "2026-09-23", "2026-09-24"],
        "branch": ["  kathmandu ", "Pokhara", "kathmandu", "  Lalitpur  ", "Pokhara"],
        "item": ["Espresso", "Latte", "Cappuccino", "Mocha", "Latte"],
        "qty": [2, 1, None, -3, 4],  # Notice the empty and negative values
        "price": [180, 250, 220, 280, 250]
    }
    pd.DataFrame(dummy_data).to_csv(csv_file, index=False)
    print("Created dummy raw_sales.csv for testing.")

# Read CSV
df = pd.read_csv(csv_file)
print("Original data:")
print(df)

# Clean up
df["branch"] = df["branch"].astype(str).str.strip().str.capitalize()
df["item"] = df["item"].astype(str).str.strip().str.capitalize()

# Fix dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Clean up bad rows
# Drop rows where quantity or date is missing
df = df.dropna(subset=["qty", "date"])

# Remove invalid orders
df = df[df["qty"] > 0]
df["qty"] = df["qty"].astype(int)

# Financial calculations (13% VAT)
df["subtotal"] = df["qty"] * df["price"]
df["vat"] = (df["subtotal"] * 0.13).round(2)
df["total"] = df["subtotal"] + df["vat"]

print("\nCleaned transactions:")
print(df)

# Make simple summaries
# Total sales by branch
branch_report = df.groupby("branch")[["qty", "total"]].sum().reset_index()
branch_report.columns = ["Branch", "Total Items Sold", "Total Revenue"]

# Total sales by product
item_report = df.groupby("item")[["qty", "total"]].sum().reset_index()
item_report = item_report.sort_values(by="total", ascending=False)
item_report.columns = ["Item", "Units Sold", "Revenue"]

print("\nBranch Summary:")
print(branch_report)

# Save to Excel with multiple sheets
output_file = Path("data/sales_report.xlsx")
with pd.ExcelWriter(output_file) as writer:
    df.to_excel(writer, sheet_name="Cleaned Data", index=False)
    branch_report.to_excel(writer, sheet_name="Branch Summary", index=False)
    item_report.to_excel(writer, sheet_name="Item Summary", index=False)

print(f"\nDone! Saved clean report to {output_file}")