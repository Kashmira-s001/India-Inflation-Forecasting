import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RBI_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "rbi_key_rates.xlsx"
)


# ============================================================
# 2. CHECK FILE
# ============================================================

print("=" * 60)
print("RBI KEY RATES FILE INSPECTION")
print("=" * 60)

print(f"File exists: {RBI_FILE.exists()}")


# ============================================================
# 3. INSPECT WORKBOOK
# ============================================================

excel = pd.ExcelFile(RBI_FILE)

print("\nSheets:")
print(excel.sheet_names)


# ============================================================
# 4. INSPECT EACH SHEET
# ============================================================

for sheet in excel.sheet_names:

    df = pd.read_excel(
        RBI_FILE,
        sheet_name=sheet,
        header=None
    )

    print("\n" + "-" * 60)
    print(f"Sheet: {sheet}")
    print("-" * 60)

    print(f"Shape: {df.shape}")

    print("\nFirst 15 rows:")
    print(
        df.head(15).to_string(
            index=False,
            header=False
        )
    )