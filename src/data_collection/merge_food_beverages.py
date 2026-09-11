from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

ECONOMIC_FILE = (
    PROCESSED_DIR / "economic_master_enriched.csv"
)

FOOD_FILE = (
    PROCESSED_DIR / "food_beverages_master.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR / "final_economic_master.csv"
)


# ============================================================
# LOAD DATASETS
# ============================================================

print("Loading datasets...")

economic_df = pd.read_csv(
    ECONOMIC_FILE,
    parse_dates=["date"]
)

food_df = pd.read_csv(
    FOOD_FILE,
    parse_dates=["date"]
)


print("\nEconomic dataset shape:", economic_df.shape)
print("Food & Beverages dataset shape:", food_df.shape)


# ============================================================
# CHECK DATE RANGES
# ============================================================

print("\nEconomic dataset date range:")
print(
    economic_df["date"].min(),
    "→",
    economic_df["date"].max()
)

print("\nFood & Beverages dataset date range:")
print(
    food_df["date"].min(),
    "→",
    food_df["date"].max()
)


# ============================================================
# MERGE DATASETS
# ============================================================

print("\nMerging Food & Beverages data...")

final_df = economic_df.merge(
    food_df,
    on="date",
    how="left"
)


# ============================================================
# SORT DATA
# ============================================================

final_df = (
    final_df
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL ECONOMIC MASTER DATASET VALIDATION")
print("=" * 60)

print("\nShape:")
print(final_df.shape)

print("\nDate range:")
print(
    final_df["date"].min().strftime("%Y-%m-%d"),
    "→",
    final_df["date"].max().strftime("%Y-%m-%d")
)

print("\nDuplicate dates:")
print(final_df["date"].duplicated().sum())

print("\nMissing values:")
print(final_df.isnull().sum())

print("\nFirst 5 rows:")
print(final_df.head().to_string(index=False))

print("\nLast 5 rows:")
print(final_df.tail().to_string(index=False))


# ============================================================
# SAVE FINAL DATASET
# ============================================================

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 60)
print("FINAL ECONOMIC MASTER DATASET CREATED")
print("=" * 60)

print(f"\nRows: {len(final_df)}")
print(f"Columns: {len(final_df.columns)}")
print(f"Output: {OUTPUT_FILE}")