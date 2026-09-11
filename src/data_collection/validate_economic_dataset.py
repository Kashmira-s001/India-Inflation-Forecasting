import pandas as pd
from pathlib import Path


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "economic_master.csv"
)


# ============================================================
# LOAD
# ============================================================

economic = pd.read_csv(FILE)

economic["date"] = pd.to_datetime(economic["date"])


print("=" * 60)
print("ECONOMIC MASTER DATA VALIDATION")
print("=" * 60)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n--- BASIC INFORMATION ---")

print("Rows:", len(economic))

print("Columns:")
print(economic.columns.tolist())

print(
    "Date range:",
    economic["date"].min().date(),
    "→",
    economic["date"].max().date()
)


# ============================================================
# DUPLICATES
# ============================================================

print("\n--- DUPLICATE CHECK ---")

print(
    "Duplicate dates:",
    economic["date"].duplicated().sum()
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n--- MISSING VALUE CHECK ---")

print(economic.isna().sum())


# ============================================================
# MONTHLY CONTINUITY
# ============================================================

print("\n--- MONTHLY CONTINUITY CHECK ---")

expected_dates = pd.date_range(
    start=economic["date"].min(),
    end=economic["date"].max(),
    freq="MS"
)

actual_dates = pd.DatetimeIndex(
    economic["date"]
)

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
    len(actual_dates)
)

print(
    "Missing months:",
    len(missing_dates)
)

print(
    "Extra dates:",
    len(extra_dates)
)


# ============================================================
# NUMERIC CHECK
# ============================================================

print("\n--- NUMERIC DATA CHECK ---")

for column in [
    "cpi_index",
    "inflation",
    "wpi_inflation",
    "repo_rate"
]:

    print(
        f"{column} numeric:",
        pd.api.types.is_numeric_dtype(
            economic[column]
        )
    )


# ============================================================
# RANGE CHECKS
# ============================================================

print("\n--- RANGE CHECK ---")

print(
    f"CPI index: "
    f"{economic['cpi_index'].min():.2f}"
    f" → "
    f"{economic['cpi_index'].max():.2f}"
)

print(
    f"CPI inflation: "
    f"{economic['inflation'].min():.2f}%"
    f" → "
    f"{economic['inflation'].max():.2f}%"
)

print(
    f"WPI inflation: "
    f"{economic['wpi_inflation'].min():.2f}%"
    f" → "
    f"{economic['wpi_inflation'].max():.2f}%"
)

print(
    f"Repo rate: "
    f"{economic['repo_rate'].min():.2f}%"
    f" → "
    f"{economic['repo_rate'].max():.2f}%"
)


# ============================================================
# LATEST OBSERVATIONS
# ============================================================

print("\n--- LATEST OBSERVATIONS ---")

print(
    economic.tail(15).to_string(index=False)
)


print("\n" + "=" * 60)
print("ECONOMIC MASTER DATA VALIDATION COMPLETED")
print("=" * 60)