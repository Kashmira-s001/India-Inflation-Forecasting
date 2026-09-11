import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WPI_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "wpi_master.csv"
)

wpi = pd.read_csv(WPI_FILE)

wpi["date"] = pd.to_datetime(wpi["date"])


print("=" * 60)
print("LONG-HISTORY WPI DATA VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# BASIC INFORMATION
# ------------------------------------------------------------

print("\n--- BASIC INFORMATION ---")

print("Rows:", len(wpi))
print("Columns:", wpi.columns.tolist())

print(
    "Date range:",
    wpi["date"].min().date(),
    "→",
    wpi["date"].max().date()
)


# ------------------------------------------------------------
# DUPLICATES
# ------------------------------------------------------------

print("\n--- DUPLICATE CHECK ---")

print(
    "Duplicate dates:",
    wpi["date"].duplicated().sum()
)


# ------------------------------------------------------------
# MISSING VALUES
# ------------------------------------------------------------

print("\n--- MISSING VALUE CHECK ---")

print(
    wpi.isna().sum()
)


# ------------------------------------------------------------
# MONTHLY CONTINUITY
# ------------------------------------------------------------

print("\n--- MONTHLY CONTINUITY CHECK ---")

expected_dates = pd.date_range(
    start=wpi["date"].min(),
    end=wpi["date"].max(),
    freq="MS"
)

actual_dates = pd.DatetimeIndex(
    wpi["date"]
)

missing_dates = expected_dates.difference(
    actual_dates
)

extra_dates = actual_dates.difference(
    expected_dates
)

print("Expected observations:", len(expected_dates))
print("Actual observations:", len(actual_dates))

print("Missing months:", len(missing_dates))
print("Extra dates:", len(extra_dates))

if len(missing_dates) > 0:
    print("\nMissing dates:")
    print(missing_dates)


# ------------------------------------------------------------
# NUMERIC CHECK
# ------------------------------------------------------------

print("\n--- NUMERIC DATA CHECK ---")

print(
    "WPI inflation numeric:",
    pd.api.types.is_numeric_dtype(
        wpi["wpi_inflation"]
    )
)


# ------------------------------------------------------------
# INFLATION RANGE
# ------------------------------------------------------------

valid_inflation = wpi[
    "wpi_inflation"
].dropna()

print("\n--- WPI INFLATION RANGE ---")

print(
    f"Minimum WPI inflation: "
    f"{valid_inflation.min():.2f}%"
)

print(
    f"Maximum WPI inflation: "
    f"{valid_inflation.max():.2f}%"
)


# ------------------------------------------------------------
# FIRST VALID OBSERVATIONS
# ------------------------------------------------------------

print("\n--- FIRST VALID WPI INFLATION ---")

print(
    wpi.dropna(
        subset=["wpi_inflation"]
    ).head(10).to_string(index=False)
)


# ------------------------------------------------------------
# LATEST OBSERVATIONS
# ------------------------------------------------------------

print("\n--- LATEST OBSERVATIONS ---")

print(
    wpi.tail(15).to_string(index=False)
)


print("\n" + "=" * 60)
print("WPI DATA VALIDATION COMPLETED")
print("=" * 60)