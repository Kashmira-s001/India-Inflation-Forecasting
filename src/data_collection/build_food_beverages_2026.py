from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DIR / "food_beverages_2026.xlsx"
OUTPUT_FILE = PROCESSED_DIR / "food_beverages_2026.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading 2026 CPI dataset...")

df = pd.read_excel(INPUT_FILE)

print(f"\nOriginal shape: {df.shape}")

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# FILTER DATA
# ============================================================

# Keep only non-imputed observations
food_df = df[
    df["imputation"].eq("N")
].copy()


# ============================================================
# CREATE DATE
# ============================================================

# Convert month name to month number
food_df["month_number"] = pd.to_datetime(
    food_df["month"],
    format="%B"
).dt.month


food_df["date"] = pd.to_datetime(
    dict(
        year=food_df["year"],
        month=food_df["month_number"],
        day=1
    )
)


# ============================================================
# SORT DATA
# ============================================================

food_df = food_df.sort_values(
    ["date", "code"]
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

food_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("2026 FOOD & BEVERAGES CPI DATASET CREATED")
print("=" * 60)

print(f"\nRows: {len(food_df)}")

print(
    "\nDate range:",
    food_df["date"].min().strftime("%Y-%m-%d"),
    "→",
    food_df["date"].max().strftime("%Y-%m-%d")
)

print("\nUnique divisions:")
print(food_df["division"].unique())

print("\nUnique groups:")
print(food_df["group"].unique())

print("\nMissing values:")
print(
    food_df[
        ["date", "index", "inflation"]
    ].isnull().sum()
)

print("\nFirst 10 rows:")
print(
    food_df[
        [
            "date",
            "division",
            "group",
            "class",
            "sub_class",
            "item",
            "code",
            "index",
            "inflation"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print(f"\nOutput: {OUTPUT_FILE}")

print("\n" + "=" * 60)
print("DATASET CREATION COMPLETED")
print("=" * 60)

# ============================================================
# SEARCH FOR AGGREGATE / OVERALL ROWS
# ============================================================

print("\n" + "=" * 60)
print("SEARCHING FOR AGGREGATE ROWS")
print("=" * 60)

search_columns = ["class", "sub_class", "item"]

for column in search_columns:

    mask = food_df[column].astype(str).str.contains(
        "overall|total",
        case=False,
        na=False,
        regex=True
    )

    results = food_df[mask]

    print(f"\n--- Matches in {column} ---")

    if len(results) == 0:
        print("No matches found.")
    else:
        print(
            results[
                [
                    "date",
                    "class",
                    "sub_class",
                    "item",
                    "code",
                    "index",
                    "inflation"
                ]
            ].to_string(index=False)
        )