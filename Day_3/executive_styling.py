import os
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

DATA_FILE = "finance_report.xlsx"

# Raw dummy data to test the script from a blank state
SAMPLE_ROWS = [
    ["Invoice ID", "Client Name", "Department", "Revenue"],
    ["TXN-101", "Himalayan Tech", "Engineering", 154000],
    ["TXN-102", "Kathmandu Logistics", "Operations", 84500.5],
    ["TXN-103", "Apex Cloud", "DevOps", 210000],
    ["TXN-104", "Pokhara Media", "Design", 45200],
    ["TXN-105", "TechAxis Labs", "Security", "125000.75"],
]


def init_raw_file(filename):
  """Build an unformatted sheet if none exists."""
  wb = openpyxl.Workbook()
  ws = wb.active
  ws.title = "Summary"

  for r in SAMPLE_ROWS:
    ws.append(r)

  wb.save(filename)
  print(f"[+] Created raw file: {filename}")


def format_executive_report(filename):
  # 1. Load the workbook
  wb = openpyxl.load_workbook(filename)
  ws = wb.active

  # --- Style definitions ---
  navy_fill = PatternFill(
      start_color="1B365D", end_color="1B365D", fill_type="solid"
  )
  header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

  border_side = Side(style="thin", color="D3D3D3")
  cell_border = Border(
      left=border_side, right=border_side, top=border_side, bottom=border_side
  )

  # 2. Header row (Navy fill + bold white text)
  for col_idx in range(1, ws.max_column + 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.fill = navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

  # 3. Grid borders across all active cells
  for row in ws.iter_rows(
      min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column
  ):
    for cell in row:
      cell.border = cell_border

  # 4. Currency formatting for Revenue (Column 4)
  # Standard accounting format with NPR prefix
  for r in range(2, ws.max_row + 1):
    val_cell = ws.cell(row=r, column=4)

    # Convert string floats to real numbers so Excel can calculate them
    if isinstance(val_cell.value, str):
      try:
        val_cell.value = float(val_cell.value)
      except ValueError:
        pass

    val_cell.number_format = '"NPR "#,##0.00'
    val_cell.alignment = Alignment(horizontal="right")

  # 5. Dynamic column width auto-fit
  for col in ws.columns:
    col_letter = get_column_letter(col[0].column)
    max_len = 0

    for cell in col:
      if cell.value is None:
        continue

      # If it's a numeric revenue value, factor in currency symbol length
      if isinstance(cell.value, (int, float)):
        text_repr = f"NPR {cell.value:,.2f}"
      else:
        text_repr = str(cell.value)

      max_len = max(max_len, len(text_repr))

    # Give extra padding so Excel doesn't display '###'
    ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

  # Commit changes to disk
  wb.save(filename)
  print(f"[ok] Styled workbook saved to {filename}")


if __name__ == "__main__":
  if not os.path.exists(DATA_FILE):
    init_raw_file(DATA_FILE)

  format_executive_report(DATA_FILE)