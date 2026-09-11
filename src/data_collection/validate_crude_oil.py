import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "crude_oil_master.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(FILE_PATH)

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# VALIDATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("BRENT CRUDE OIL DATA VALIDATION")
print("=" * 60)


# BASIC INFORMATION

print("\n--- BASIC INFORMATION ---")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print(
    "Date range:",
    df["date"].min().date(),
    "→",
    df["date"].max().date()
)


# DUPLICATES

print("\n--- DUPLICATE CHECK ---")

duplicate_dates = df["date"].duplicated().sum()

print("Duplicate dates:", duplicate_dates)


# MISSING VALUES

print("\n--- MISSING VALUE CHECK ---")

print(df.isna().sum())


# MONTHLY CONTINUITY

print("\n--- MONTHLY CONTINUITY CHECK ---")

expected_dates = pd.date_range(
    start=df["date"].min(),
    end=df["date"].max(),
    freq="MS"
)

actual_dates = pd.DatetimeIndex(df["date"])

missing_months = expected_dates.difference(actual_dates)

extra_dates = actual_dates.difference(expected_dates)

print("Expected observations:", len(expected_dates))
print("Actual observations:", len(df))

print("Missing months:", len(missing_months))
print("Extra dates:", len(extra_dates))


# NUMERIC CHECK

print("\n--- NUMERIC DATA CHECK ---")

numeric_columns = [
    "brent_price_usd",
    "brent_mom_change_pct",
    "brent_yoy_change_pct"
]

for column in numeric_columns:
    print(
        f"{column} numeric:",
        pd.api.types.is_numeric_dtype(df[column])
    )


# RANGE CHECK

print("\n--- BRENT PRICE RANGE ---")

print(
    "Minimum Brent price:",
    f"${df['brent_price_usd'].min():.2f}/bbl"
)

print(
    "Maximum Brent price:",
    f"${df['brent_price_usd'].max():.2f}/bbl"
)


# FIRST OBSERVATIONS

print("\n--- FIRST OBSERVATIONS ---")

print(
    df.head(5).to_string(index=False)
)


# LATEST OBSERVATIONS

print("\n--- LATEST OBSERVATIONS ---")

print(
    df.tail(15).to_string(index=False)
)


# FINAL RESULT

print("\n" + "=" * 60)

if (
    duplicate_dates == 0
    and len(missing_months) == 0
    and df["brent_price_usd"].isna().sum() == 0
):
    print("BRENT CRUDE OIL DATA VALIDATION PASSED")
else:
    print("BRENT CRUDE OIL DATA VALIDATION NEEDS REVIEW")

print("=" * 60)