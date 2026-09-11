import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

BACK_FILE = RAW_DATA / "cpi_back_series_2013_2024.xlsx"
CURRENT_FILE = RAW_DATA / "cpi_current_jan2025_jul2026.xlsx"

OUTPUT_FILE = PROCESSED_DATA / "cpi_master.csv"


# ============================================================
# 2. CREATE PROCESSED DIRECTORY
# ============================================================

PROCESSED_DATA.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 3. LOAD HISTORICAL BACK SERIES
# ============================================================

print("Loading CPI back series...")

back_df = pd.read_excel(
    BACK_FILE,
    sheet_name="CPI Data"
)


back_df = back_df[
    [
        "year",
        "month",
        "index",
        "inflation"
    ]
].copy()


back_df.rename(
    columns={
        "index": "cpi_index"
    },
    inplace=True
)


# ============================================================
# 4. LOAD CURRENT CPI DATA
# ============================================================

print("Loading current CPI data...")

current_df = pd.read_excel(
    CURRENT_FILE,
    sheet_name="CPI Combined ",
    header=1
)


current_df.columns = [
    "year",
    "month",
    "state",
    "description",
    "cpi_index"
]


current_df = current_df[
    [
        "year",
        "month",
        "cpi_index"
    ]
].copy()


current_df["inflation"] = None


# ============================================================
# 5. COMBINE DATA
# ============================================================

print("Combining datasets...")

master_df = pd.concat(
    [
        back_df,
        current_df
    ],
    ignore_index=True
)


# ============================================================
# 6. CLEAN DATA TYPES
# ============================================================

master_df["year"] = pd.to_numeric(
    master_df["year"],
    errors="coerce"
)

master_df["cpi_index"] = pd.to_numeric(
    master_df["cpi_index"],
    errors="coerce"
)

master_df["inflation"] = pd.to_numeric(
    master_df["inflation"],
    errors="coerce"
)


# ============================================================
# 7. CREATE DATE
# ============================================================

master_df["date"] = pd.to_datetime(
    master_df["year"].astype("Int64").astype(str)
    + "-"
    + master_df["month"],
    format="%Y-%B",
    errors="coerce"
)


# ============================================================
# 8. REMOVE INVALID ROWS
# ============================================================

master_df = master_df.dropna(
    subset=["date", "cpi_index"]
)


# ============================================================
# 9. SORT CHRONOLOGICALLY
# ============================================================

master_df = (
    master_df
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# 10. REMOVE DUPLICATES
# ============================================================

master_df.drop_duplicates(
    subset=["date"],
    keep="last",
    inplace=True
)


# ============================================================
# 11. CALCULATE YEAR-ON-YEAR INFLATION
# ============================================================

master_df["calculated_inflation"] = (
    master_df["cpi_index"]
    .pct_change(periods=12)
    * 100
)


# ============================================================
# 12. USE OFFICIAL INFLATION WHEN AVAILABLE
# ============================================================

master_df["inflation_final"] = (
    master_df["inflation"]
    .fillna(master_df["calculated_inflation"])
)


# ============================================================
# 13. SELECT FINAL COLUMNS
# ============================================================

master_df = master_df[
    [
        "date",
        "year",
        "month",
        "cpi_index",
        "inflation_final"
    ]
].copy()


master_df.rename(
    columns={
        "inflation_final": "inflation"
    },
    inplace=True
)


# ============================================================
# 14. SAVE
# ============================================================

master_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 15. REPORT
# ============================================================

print("\n" + "=" * 60)
print("CPI MASTER DATASET CREATED")
print("=" * 60)

print(f"Rows: {len(master_df)}")

print(
    f"Date range: "
    f"{master_df['date'].min().date()} → "
    f"{master_df['date'].max().date()}"
)

print(f"Output: {OUTPUT_FILE}")

print("\nLast 10 observations:")

print(
    master_df
    .tail(10)
    .to_string(index=False)
)