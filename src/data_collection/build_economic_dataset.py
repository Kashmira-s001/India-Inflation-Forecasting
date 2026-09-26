import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

CPI_FILE = PROCESSED_DATA / "cpi_master.csv"
WPI_FILE = PROCESSED_DATA / "wpi_master.csv"
REPO_FILE = PROCESSED_DATA / "repo_rate_master.csv"

OUTPUT_FILE = PROCESSED_DATA / "economic_master.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading CPI...")
cpi = pd.read_csv(CPI_FILE)

print("Loading WPI...")
wpi = pd.read_csv(WPI_FILE)

print("Loading RBI repo rate...")
repo = pd.read_csv(REPO_FILE)


# ============================================================
# CONVERT DATES
# ============================================================

cpi["date"] = pd.to_datetime(cpi["date"])
wpi["date"] = pd.to_datetime(wpi["date"])
repo["date"] = pd.to_datetime(repo["date"])


# ============================================================
# SELECT REQUIRED COLUMNS
# ============================================================

# CPI is our main target series.
cpi = cpi[
    [
        "date",
        "year",
        "month",
        "cpi_index",
        "inflation"
    ]
].copy()


# WPI variables required for inflation analysis.
wpi = wpi[
    [
        "date",
        "wpi_index",
        "wpi_inflation"
    ]
].copy()


# RBI policy variable.
repo = repo[
    [
        "date",
        "repo_rate"
    ]
].copy()


# ============================================================
# SORT
# ============================================================

cpi = cpi.sort_values("date").reset_index(drop=True)
wpi = wpi.sort_values("date").reset_index(drop=True)
repo = repo.sort_values("date").reset_index(drop=True)


# ============================================================
# MERGE CPI + WPI
# ============================================================

print("\nMerging CPI and WPI...")

economic = pd.merge(
    cpi,
    wpi,
    on="date",
    how="left"
)


# ============================================================
# MERGE REPO RATE
# ============================================================

print("Merging RBI repo rate...")

economic = pd.merge(
    economic,
    repo,
    on="date",
    how="left"
)


# ============================================================
# SORT FINAL DATASET
# ============================================================

economic = (
    economic
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# SAVE
# ============================================================

economic.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("ECONOMIC MASTER DATASET CREATED")
print("=" * 60)

print(f"Rows: {len(economic)}")

print(
    f"Date range: "
    f"{economic['date'].min().date()} → "
    f"{economic['date'].max().date()}"
)

print("\nColumns:")
print(economic.columns.tolist())

print("\nMissing values:")
print(economic.isnull().sum())

print("\nFirst 5 observations:")
print(
    economic.head().to_string(index=False)
)

print("\nLatest 15 observations:")
print(
    economic.tail(15).to_string(index=False)
)

print(f"\nOutput: {OUTPUT_FILE}")