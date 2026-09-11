import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

WPI_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "monthly_index_202606.xls"
)


# ============================================================
# 2. CHECK FILE
# ============================================================

print("=" * 60)
print("HISTORICAL WPI FILE INSPECTION")
print("=" * 60)

print(f"File exists: {WPI_FILE.exists()}")


# ============================================================
# 3. INSPECT WORKBOOK
# ============================================================

excel = pd.ExcelFile(WPI_FILE)

print("\nSheets:")
print(excel.sheet_names)


# ============================================================
# 4. INSPECT EACH SHEET
# ============================================================

for sheet in excel.sheet_names:

    df = pd.read_excel(
        WPI_FILE,
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