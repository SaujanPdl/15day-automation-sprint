import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import pandas as pd


def resource_path(relative_path: str) -> Path:
  """Deliverable 3: Fix relative file paths for PyInstaller bundled configurations.

  When running as a compiled onefile exe, sys._MEIPASS points to the temp
  folder.
  When running normally in development, it uses the script's local directory.
  """
  try:
    base_path = Path(sys._MEIPASS)
  except AttributeError:
    base_path = Path(__file__).resolve().parent

  return base_path / relative_path


def get_base_dir() -> Path:
  """Gets the folder where the .exe itself lives on the client's machine."""
  if getattr(sys, "frozen", False):
    return Path(sys.executable).resolve().parent
  return Path(__file__).resolve().parent


def run_standalone_automation():
  # Hide root tkinter window
  root = tk.Tk()
  root.withdraw()

  base_dir = get_base_dir()
  input_dir = base_dir / "input_data"
  output_file = base_dir / "automated_summary_report.xlsx"

  # If input folder doesn't exist, create it with a sample file
  if not input_dir.exists():
    input_dir.mkdir(parents=True, exist_ok=True)
    sample_df = pd.DataFrame({
        "Invoice_ID": ["INV-1001", "INV-1002", "INV-1003"],
        "Client": ["Apex Corp", "Tech Innovators", "Summit Retail"],
        "Revenue": [125000, 89000, 45000],
    })
    sample_df.to_excel(input_dir / "sample_sales.xlsx", index=False)
    messagebox.showinfo(
        "Setup Complete",
        f"Created an 'input_data' folder at:\n{input_dir}\n\nAdd your Excel"
        " files there and run this application again.",
    )
    return

  excel_files = list(input_dir.glob("*.xlsx"))
  if not excel_files:
    messagebox.showwarning(
        "No Files Found",
        f"No .xlsx files found in:\n{input_dir}\n\nPlease add files to process.",
    )
    return

  # Process and combine files
  frames = []
  for f in excel_files:
    df = pd.read_excel(f)
    df["Source_File"] = f.name
    frames.append(df)

  combined = pd.concat(frames, ignore_index=True)

  # Write output
  combined.to_excel(output_file, index=False)

  messagebox.showinfo(
      "Process Finished",
      f"Successfully processed {len(excel_files)} files ({len(combined)}"
      f" records)!\n\nReport generated at:\n{output_file}",
  )


if __name__ == "__main__":
  run_standalone_automation()