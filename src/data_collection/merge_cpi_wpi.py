import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

CPI_FILE = PROCESSED_DATA / "cpi_master.csv"
WPI_FILE = PROCESSED_DATA / "wpi_master.csv"

OUTPUT_FILE = PROCESSED_DATA / "cpi_wpi_master.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

print("Loading CPI dataset...")
cpi = pd.read_csv(CPI_FILE)

print("Loading WPI dataset...")
wpi = pd.read_csv(WPI_FILE)


# ============================================================
# 3. CONVERT DATES
# ============================================================

cpi["date"] = pd.to_datetime(cpi["date"])
wpi["date"] = pd.to_datetime(wpi["date"])


# ============================================================
# 4. MERGE DATASETS
# ============================================================

print("\nMerging CPI and WPI...")

merged = pd.merge(
    cpi,
    wpi,
    on="date",
    how="inner"
)


# ============================================================
# 5. SORT
# ============================================================

merged = merged.sort_values(
    "date"
).reset_index(drop=True)


# ============================================================
# 6. SAVE
# ============================================================

merged.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 7. REPORT
# ============================================================

print("\n" + "=" * 60)
print("CPI + WPI DATASET CREATED")
print("=" * 60)

print(f"Rows: {len(merged)}")
print(f"Columns: {merged.columns.tolist()}")

print(
    f"Date range: "
    f"{merged['date'].min().date()} → "
    f"{merged['date'].max().date()}"
)

print("\nMissing values:")
print(merged.isnull().sum())

print("\nFirst 5 observations:")
print(
    merged.head().to_string(index=False)
)

print("\nLatest 10 observations:")
print(
    merged.tail(10).to_string(index=False)
)

print(f"\nOutput: {OUTPUT_FILE}")