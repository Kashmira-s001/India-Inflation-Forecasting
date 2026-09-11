import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "exchange_rate_master.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["date"]
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("USD/INR EXCHANGE RATE DATA VALIDATION")
print("=" * 60)


print("\n--- BASIC INFORMATION ---")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print(
    "Date range:",
    df["date"].min().date(),
    "→",
    df["date"].max().date()
)


# ------------------------------------------------------------

print("\n--- DUPLICATE CHECK ---")

duplicate_dates = df["date"].duplicated().sum()

print(
    "Duplicate dates:",
    duplicate_dates
)


# ------------------------------------------------------------

print("\n--- MISSING VALUE CHECK ---")

print(
    df.isna().sum()
)


# ------------------------------------------------------------

print("\n--- MONTHLY CONTINUITY CHECK ---")

expected_dates = pd.date_range(
    start=df["date"].min(),
    end=df["date"].max(),
    freq="MS"
)

actual_dates = pd.DatetimeIndex(df["date"])

missing_dates = expected_dates.difference(
    actual_dates
)

extra_dates = actual_dates.difference(
    expected_dates
)

print(
    "Expected observations:",
    len(expected_dates)
)

print(
    "Actual observations:",
    len(df)
)

print(
    "Missing months:",
    len(missing_dates)
)

print(
    "Extra dates:",
    len(extra_dates)
)


# ------------------------------------------------------------

print("\n--- NUMERIC DATA CHECK ---")

numeric_columns = [
    "usd_inr_rate",
    "usd_inr_mom_change_pct",
    "usd_inr_yoy_change_pct"
]

for column in numeric_columns:

    is_numeric = pd.api.types.is_numeric_dtype(
        df[column]
    )

    print(
        f"{column} numeric:",
        is_numeric
    )


# ------------------------------------------------------------

print("\n--- EXCHANGE RATE RANGE ---")

print(
    "Minimum USD/INR rate:",
    df["usd_inr_rate"].min()
)

print(
    "Maximum USD/INR rate:",
    df["usd_inr_rate"].max()
)


# ------------------------------------------------------------

print("\n--- FIRST OBSERVATIONS ---")

print(
    df.head(5).to_string(
        index=False
    )
)


# ------------------------------------------------------------

print("\n--- LATEST OBSERVATIONS ---")

print(
    df.tail(15).to_string(
        index=False
    )
)


# ============================================================

print("\n" + "=" * 60)
print("USD/INR EXCHANGE RATE DATA VALIDATION COMPLETED")
print("=" * 60)