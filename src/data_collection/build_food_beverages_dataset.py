import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "food_beverages_master.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "food_beverages_master.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading Food and Beverages dataset...")

df = pd.read_excel(RAW_FILE)

print("\nOriginal shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# INSPECT DATA BEFORE CLEANING
# ============================================================

print("\nData types:")
print(df.dtypes)


# ============================================================
# SAVE TEMPORARILY FOR INSPECTION
# ============================================================

print("\n" + "=" * 60)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 60)

# ============================================================
# INSPECT FILTER VALUES
# ============================================================

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

print("\nStates:")
print(df["state"].unique())

print("\nSectors:")
print(df["sector"].unique())

print("\nGroups:")
print(df["group"].unique())

print("\nSubgroups:")
print(df["subgroup"].unique())

print("\nBase years:")
print(df["baseyear"].unique())

print("\nYears:")
print(sorted(df["year"].unique()))