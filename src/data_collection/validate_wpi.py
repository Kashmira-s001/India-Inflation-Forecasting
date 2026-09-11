import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "wpi_master.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_FILE)

df["date"] = pd.to_datetime(df["date"])


print("=" * 60)
print("WPI DATA VALIDATION")
print("=" * 60)


# ============================================================
# 3. BASIC INFORMATION
# ============================================================

print("\n--- BASIC INFORMATION ---")

print(f"Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

print(
    f"Date range: "
    f"{df['date'].min().date()} → "
    f"{df['date'].max().date()}"
)


# ============================================================
# 4. DUPLICATE CHECK
# ============================================================

print("\n--- DUPLICATE CHECK ---")

duplicates = df["date"].duplicated().sum()

print(f"Duplicate dates: {duplicates}")


# ============================================================
# 5. MISSING VALUE CHECK
# ============================================================

print("\n--- MISSING VALUE CHECK ---")

print(df.isnull().sum())


# ============================================================
# 6. MONTHLY CONTINUITY
# ============================================================

print("\n--- MONTHLY CONTINUITY CHECK ---")

expected_dates = pd.date_range(
    start=df["date"].min(),
    end=df["date"].max(),
    freq="MS"
)

actual_dates = pd.DatetimeIndex(
    df["date"].sort_values()
)

missing_months = expected_dates.difference(
    actual_dates
)

extra_dates = actual_dates.difference(
    expected_dates
)

print(f"Expected observations: {len(expected_dates)}")
print(f"Actual observations: {len(actual_dates)}")
print(f"Missing months: {len(missing_months)}")
print(f"Extra dates: {len(extra_dates)}")

if len(missing_months) > 0:
    print("\nMissing months:")
    print(missing_months)


# ============================================================
# 7. NUMERIC CHECK
# ============================================================

print("\n--- NUMERIC DATA CHECK ---")

print(
    f"WPI index numeric: "
    f"{pd.api.types.is_numeric_dtype(df['wpi_index'])}"
)

print(
    f"WPI inflation numeric: "
    f"{pd.api.types.is_numeric_dtype(df['wpi_inflation'])}"
)


# ============================================================
# 8. RANGE CHECK
# ============================================================

print("\n--- WPI INDEX RANGE ---")

print(f"Minimum WPI index: {df['wpi_index'].min()}")
print(f"Maximum WPI index: {df['wpi_index'].max()}")


print("\n--- WPI INFLATION RANGE ---")

print(
    f"Minimum WPI inflation: "
    f"{df['wpi_inflation'].min():.2f}%"
)

print(
    f"Maximum WPI inflation: "
    f"{df['wpi_inflation'].max():.2f}%"
)


# ============================================================
# 9. LATEST OBSERVATIONS
# ============================================================

print("\n--- LATEST OBSERVATIONS ---")

print(
    df.tail(12).to_string(index=False)
)


# ============================================================
# 10. FINAL RESULT
# ============================================================

print("\n" + "=" * 60)

if (
    duplicates == 0
    and len(missing_months) == 0
    and len(extra_dates) == 0
):
    print("WPI DATA VALIDATION PASSED")
else:
    print("WPI DATA VALIDATION NEEDS ATTENTION")

print("=" * 60)