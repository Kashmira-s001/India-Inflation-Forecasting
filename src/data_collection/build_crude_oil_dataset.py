import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "crude_oil"
    / "CMO-Historical-Data-Monthly.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crude_oil_master.csv"
)


# ============================================================
# LOAD WORLD BANK MONTHLY PRICES
# ============================================================

print("Loading World Bank commodity data...")

raw = pd.read_excel(
    RAW_FILE,
    sheet_name="Monthly Prices",
    header=4
)


# ============================================================
# INSPECT REQUIRED COLUMNS
# ============================================================

print("\nColumns containing crude oil:")
print(
    [
        col
        for col in raw.columns
        if "Crude oil" in str(col)
    ]
)


# ============================================================
# SELECT DATE + BRENT
# ============================================================

crude = raw[
    [
        raw.columns[0],
        "Crude oil, Brent"
    ]
].copy()

crude.columns = [
    "raw_date",
    "brent_price_usd"
]


# ============================================================
# CLEAN DATE
# ============================================================

# Remove the units row, where raw_date is missing
crude = crude.dropna(subset=["raw_date"])

# Convert World Bank format:
# 2013M01 -> 2013-01-01

crude["date"] = pd.to_datetime(
    crude["raw_date"].astype(str),
    format="%YM%m",
    errors="coerce"
)

# ============================================================
# CLEAN PRICE
# ============================================================

crude["brent_price_usd"] = pd.to_numeric(
    crude["brent_price_usd"],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID ROWS
# ============================================================

crude = crude.dropna(
    subset=["date", "brent_price_usd"]
)


# ============================================================
# KEEP PROJECT PERIOD
# ============================================================

crude = crude[
    (crude["date"] >= "2013-01-01")
    & (crude["date"] <= "2026-07-01")
].copy()


# ============================================================
# SORT
# ============================================================

crude = (
    crude
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# CREATE PRICE CHANGE FEATURES
# ============================================================

crude["brent_mom_change_pct"] = (
    crude["brent_price_usd"]
    .pct_change()
    * 100
)

crude["brent_yoy_change_pct"] = (
    crude["brent_price_usd"]
    .pct_change(periods=12)
    * 100
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

crude[
    [
        "date",
        "brent_price_usd",
        "brent_mom_change_pct",
        "brent_yoy_change_pct"
    ]
].to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("BRENT CRUDE OIL MASTER DATASET CREATED")
print("=" * 60)

print("Rows:", len(crude))

print(
    "Date range:",
    crude["date"].min().date(),
    "→",
    crude["date"].max().date()
)

print(
    "Missing Brent prices:",
    crude["brent_price_usd"].isna().sum()
)

print(
    "Missing MoM change:",
    crude["brent_mom_change_pct"].isna().sum()
)

print(
    "Missing YoY change:",
    crude["brent_yoy_change_pct"].isna().sum()
)

print("\nFirst 10 observations:")
print(
    crude.head(10).to_string(index=False)
)

print("\nLatest 10 observations:")
print(
    crude.tail(10).to_string(index=False)
)

print("\nOutput:", OUTPUT_FILE)