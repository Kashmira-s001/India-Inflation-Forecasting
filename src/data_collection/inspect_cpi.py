import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"

BACK_SERIES_FILE = RAW_DATA / "C:/Users/kashm/Documents/Inflation-Forecasting/data/raw/cpi_back_series_2013_2024.xlsx"
CURRENT_FILE = RAW_DATA / "C:/Users/kashm/Documents/Inflation-Forecasting/data/raw/cpi_current_jan2025_jul2026.xlsx"


# --------------------------------------------------
# 2. Check that files exist
# --------------------------------------------------

print("=" * 60)
print("CHECKING FILES")
print("=" * 60)

print(f"Back series exists: {BACK_SERIES_FILE.exists()}")
print(f"Current data exists: {CURRENT_FILE.exists()}")


# --------------------------------------------------
# 3. Inspect back-series workbook
# --------------------------------------------------

print("\n" + "=" * 60)
print("BACK SERIES")
print("=" * 60)

back_excel = pd.ExcelFile(BACK_SERIES_FILE)

print("\nSheets:")
print(back_excel.sheet_names)

for sheet in back_excel.sheet_names:
    df = pd.read_excel(BACK_SERIES_FILE, sheet_name=sheet)

    print(f"\n--- Sheet: {sheet} ---")
    print(f"Shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())


# --------------------------------------------------
# 4. Inspect current-data workbook
# --------------------------------------------------

print("\n" + "=" * 60)
print("CURRENT DATA")
print("=" * 60)

current_excel = pd.ExcelFile(CURRENT_FILE)

print("\nSheets:")
print(current_excel.sheet_names)

for sheet in current_excel.sheet_names:
    df = pd.read_excel(CURRENT_FILE, sheet_name=sheet)

    print(f"\n--- Sheet: {sheet} ---")
    print(f"Shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())