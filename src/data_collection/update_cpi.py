import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

MASTER_FILE = PROCESSED_DATA / "cpi_master.csv"

# New official CPI file
LATEST_FILE = RAW_DATA / "cpi_latest.xlsx"


# ============================================================
# 2. CHECK FILES
# ============================================================

if not MASTER_FILE.exists():
    raise FileNotFoundError(
        f"Existing CPI master not found:\n{MASTER_FILE}"
    )

if not LATEST_FILE.exists():
    raise FileNotFoundError(
        f"Latest CPI file not found:\n{LATEST_FILE}\n\n"
        "Place the newest official CPI Excel file in "
        "data/raw/ and rename it to cpi_latest.xlsx"
    )


# ============================================================
# 3. LOAD EXISTING MASTER
# ============================================================

print("Loading existing CPI master...")

master_df = pd.read_csv(
    MASTER_FILE,
    parse_dates=["date"]
)


# ============================================================
# 4. LOAD NEW OFFICIAL DATA
# ============================================================

print("Loading latest official CPI data...")

latest_df = pd.read_excel(
    LATEST_FILE,
    sheet_name="CPI Combined ",
    header=1
)


# ============================================================
# 5. CHECK COLUMNS
# ============================================================

latest_df.columns = [
    "year",
    "month",
    "state",
    "description",
    "cpi_index"
]


# ============================================================
# 6. SELECT REQUIRED COLUMNS
# ============================================================

latest_df = latest_df[
    [
        "year",
        "month",
        "cpi_index"
    ]
].copy()


latest_df["inflation"] = None


# ============================================================
# 7. CLEAN DATA TYPES
# ============================================================

latest_df["year"] = pd.to_numeric(
    latest_df["year"],
    errors="coerce"
)

latest_df["cpi_index"] = pd.to_numeric(
    latest_df["cpi_index"],
    errors="coerce"
)


# ============================================================
# 8. CREATE DATE
# ============================================================

latest_df["date"] = pd.to_datetime(
    latest_df["year"].astype("Int64").astype(str)
    + "-"
    + latest_df["month"],
    format="%Y-%B",
    errors="coerce"
)


# ============================================================
# 9. REMOVE INVALID ROWS
# ============================================================

latest_df = latest_df.dropna(
    subset=["date", "cpi_index"]
)


# ============================================================
# 10. KEEP REQUIRED COLUMNS
# ============================================================

latest_df = latest_df[
    [
        "date",
        "year",
        "month",
        "cpi_index",
        "inflation"
    ]
]


# ============================================================
# 11. COMBINE OLD + NEW
# ============================================================

print("Updating CPI master...")

combined_df = pd.concat(
    [
        master_df,
        latest_df
    ],
    ignore_index=True
)


# ============================================================
# 12. SORT
# ============================================================

combined_df = (
    combined_df
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# 13. REMOVE DUPLICATES
# ============================================================

combined_df.drop_duplicates(
    subset=["date"],
    keep="last",
    inplace=True
)


# ============================================================
# 14. RECALCULATE INFLATION
# ============================================================

combined_df["calculated_inflation"] = (
    combined_df["cpi_index"]
    .pct_change(periods=12)
    * 100
)


combined_df["inflation_final"] = (
    combined_df["inflation"]
    .fillna(combined_df["calculated_inflation"])
)


# ============================================================
# 15. FINAL COLUMNS
# ============================================================

combined_df = combined_df[
    [
        "date",
        "year",
        "month",
        "cpi_index",
        "inflation_final"
    ]
].copy()


combined_df.rename(
    columns={
        "inflation_final": "inflation"
    },
    inplace=True
)


# ============================================================
# 16. SAVE UPDATED MASTER
# ============================================================

combined_df.to_csv(
    MASTER_FILE,
    index=False
)


# ============================================================
# 17. REPORT
# ============================================================

print("\n" + "=" * 60)
print("CPI MASTER DATASET UPDATED")
print("=" * 60)

print(f"Rows: {len(combined_df)}")

print(
    f"Date range: "
    f"{combined_df['date'].min().date()} → "
    f"{combined_df['date'].max().date()}"
)

print(f"Output: {MASTER_FILE}")

print("\nLatest observations:")

print(
    combined_df
    .tail(10)
    .to_string(index=False)
)