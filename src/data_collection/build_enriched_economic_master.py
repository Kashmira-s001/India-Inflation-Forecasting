import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ECONOMIC_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "economic_master.csv"
)

CRUDE_OIL_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crude_oil_master.csv"
)

EXCHANGE_RATE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "exchange_rate_master.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "economic_master_enriched.csv"
)


# ============================================================
# LOAD DATASETS
# ============================================================

print("Loading datasets...")

economic = pd.read_csv(
    ECONOMIC_FILE,
    parse_dates=["date"]
)

crude_oil = pd.read_csv(
    CRUDE_OIL_FILE,
    parse_dates=["date"]
)

exchange_rate = pd.read_csv(
    EXCHANGE_RATE_FILE,
    parse_dates=["date"]
)


# ============================================================
# KEEP REQUIRED COLUMNS
# ============================================================

crude_oil = crude_oil[
    [
        "date",
        "brent_price_usd",
        "brent_mom_change_pct",
        "brent_yoy_change_pct"
    ]
]

exchange_rate = exchange_rate[
    [
        "date",
        "usd_inr_rate",
        "usd_inr_mom_change_pct",
        "usd_inr_yoy_change_pct"
    ]
]


# ============================================================
# MERGE DATASETS
# ============================================================

print("Merging crude oil data...")

enriched = economic.merge(
    crude_oil,
    on="date",
    how="left"
)

print("Merging USD/INR exchange rate data...")

enriched = enriched.merge(
    exchange_rate,
    on="date",
    how="left"
)


# ============================================================
# SORT
# ============================================================

enriched = (
    enriched
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

enriched.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("ENRICHED ECONOMIC MASTER DATASET CREATED")
print("=" * 60)

print("\nShape:")
print(enriched.shape)

print("\nDate range:")
print(
    enriched["date"].min().date(),
    "→",
    enriched["date"].max().date()
)

print("\nColumns:")
print(enriched.columns.tolist())


print("\n--- MISSING VALUES ---")
print(
    enriched.isna().sum()
)


print("\n--- FIRST 5 ROWS ---")
print(
    enriched.head().to_string(
        index=False
    )
)


print("\n--- LAST 5 ROWS ---")
print(
    enriched.tail().to_string(
        index=False
    )
)


print("\nOutput:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("ENRICHED ECONOMIC MASTER DATASET COMPLETED")
print("=" * 60)