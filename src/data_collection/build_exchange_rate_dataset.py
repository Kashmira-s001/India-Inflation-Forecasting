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
    / "exchange_rate"
    / "EXINUS.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "exchange_rate_master.csv"
)


# ============================================================
# LOAD FRED DATA
# ============================================================

print("Loading FRED USD/INR data...")

df = pd.read_csv(RAW_FILE)


# ============================================================
# RENAME COLUMNS
# ============================================================

df = df.rename(
    columns={
        "observation_date": "date",
        "EXINUS": "usd_inr_rate"
    }
)


# ============================================================
# CLEAN DATE
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# ============================================================
# CLEAN EXCHANGE RATE
# ============================================================

df["usd_inr_rate"] = pd.to_numeric(
    df["usd_inr_rate"],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID ROWS
# ============================================================

df = df.dropna(
    subset=["date", "usd_inr_rate"]
)


# ============================================================
# KEEP PROJECT PERIOD
# ============================================================

df = df[
    (df["date"] >= "2013-01-01")
    & (df["date"] <= "2026-08-01")
].copy()


# ============================================================
# SORT
# ============================================================

df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# CREATE CHANGE FEATURES
# ============================================================

df["usd_inr_mom_change_pct"] = (
    df["usd_inr_rate"]
    .pct_change()
    * 100
)

df["usd_inr_yoy_change_pct"] = (
    df["usd_inr_rate"]
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

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("USD/INR EXCHANGE RATE MASTER DATASET CREATED")
print("=" * 60)

print("Rows:", len(df))

print(
    "Date range:",
    df["date"].min().date(),
    "→",
    df["date"].max().date()
)

print(
    "Missing exchange rates:",
    df["usd_inr_rate"].isna().sum()
)

print(
    "Missing MoM change:",
    df["usd_inr_mom_change_pct"].isna().sum()
)

print(
    "Missing YoY change:",
    df["usd_inr_yoy_change_pct"].isna().sum()
)

print("\nFirst 10 observations:")
print(
    df.head(10).to_string(index=False)
)

print("\nLatest 10 observations:")
print(
    df.tail(10).to_string(index=False)
)

print("\nOutput:", OUTPUT_FILE)