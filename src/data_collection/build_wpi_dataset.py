import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HISTORICAL_FILE = (
    PROJECT_ROOT / "data" / "raw" / "monthly_index_202606.xls"
)

CURRENT_FILE = (
    PROJECT_ROOT / "data" / "raw" / "wpi_monthly_index_202608.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "wpi_master.csv"
)


# ============================================================
# LOAD HISTORICAL WPI
# ============================================================

print("Loading historical WPI data...")

historical = pd.read_excel(
    HISTORICAL_FILE,
    sheet_name="MONTHLY_INDEX"
)

print("Historical shape:", historical.shape)


# ============================================================
# SELECT ALL COMMODITIES
# ============================================================

historical_all = historical[
    historical["COMM_NAME"].astype(str).str.strip().str.lower()
    == "all commodities"
].copy()

if historical_all.empty:
    raise ValueError("All commodities series not found in historical WPI file.")


# ============================================================
# EXTRACT MONTHLY HISTORICAL INDEX
# ============================================================

month_columns = [
    col for col in historical_all.columns
    if str(col).startswith("INDX")
]

historical_long = historical_all[
    month_columns
].T.reset_index()

historical_long.columns = ["raw_date", "wpi_index"]

historical_long["date"] = pd.to_datetime(
    historical_long["raw_date"].str.extract(r"INDX(\d{2})(\d{4})")[1]
    + "-"
    + historical_long["raw_date"].str.extract(r"INDX(\d{2})(\d{4})")[0]
    + "-01"
)

historical_long["wpi_index"] = pd.to_numeric(
    historical_long["wpi_index"],
    errors="coerce"
)

historical_long = historical_long[
    ["date", "wpi_index"]
].dropna(subset=["wpi_index"])

historical_long = historical_long.sort_values("date")


# ============================================================
# CALCULATE HISTORICAL WPI INFLATION
# ============================================================

historical_long["wpi_inflation"] = (
    historical_long["wpi_index"]
    .pct_change(periods=12)
    * 100
)


# We only need historical inflation up to March 2024.
# From April 2024 onward, the newer 2022-23-base WPI
# dataset will provide the official latest series.

historical_part = historical_long[
    historical_long["date"] < "2024-04-01"
].copy()


# ============================================================
# LOAD CURRENT WPI
# ============================================================

print("Loading current WPI data...")

current = pd.read_excel(
    CURRENT_FILE,
    sheet_name="Sheet3"
)

print("Current shape:", current.shape)


# ============================================================
# SELECT ALL COMMODITIES
# ============================================================

current_all = current[
    current["Commodity Name"].astype(str).str.strip().str.lower()
    == "all commodities"
].copy()

if current_all.empty:
    raise ValueError("All commodities series not found in current WPI file.")


# ============================================================
# EXTRACT CURRENT MONTHLY INDEX
# ============================================================

current_month_columns = [
    col for col in current_all.columns
    if str(col)[:3] in [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
]

current_long = current_all[
    current_month_columns
].T.reset_index()

current_long.columns = ["raw_date", "wpi_index"]

current_long["date"] = pd.to_datetime(
    current_long["raw_date"],
    format="%b-%y"
) + pd.offsets.MonthBegin(0)

current_long["wpi_index"] = pd.to_numeric(
    current_long["wpi_index"],
    errors="coerce"
)

current_long = current_long[
    ["date", "wpi_index"]
].dropna(subset=["wpi_index"])

current_long = current_long.sort_values("date")


# ============================================================
# CALCULATE CURRENT WPI INFLATION
# ============================================================

current_long["wpi_inflation"] = (
    current_long["wpi_index"]
    .pct_change(periods=12)
    * 100
)


# ============================================================
# KEEP CURRENT SERIES FROM APRIL 2024
# ============================================================

current_part = current_long[
    current_long["date"] >= "2024-04-01"
].copy()


# ============================================================
# COMBINE HISTORICAL + CURRENT
# ============================================================

print("Combining historical and current WPI inflation...")

wpi_master = pd.concat(
    [
        historical_part[
            ["date", "wpi_inflation"]
        ],
        current_part[
            ["date", "wpi_inflation"]
        ]
    ],
    ignore_index=True
)

wpi_master = wpi_master.sort_values("date")

wpi_master = wpi_master.drop_duplicates(
    subset="date",
    keep="last"
)

wpi_master = wpi_master.reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

wpi_master.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print()
print("=" * 60)
print("LONG-HISTORY WPI MASTER DATASET CREATED")
print("=" * 60)

print("Rows:", len(wpi_master))
print(
    "Date range:",
    wpi_master["date"].min().date(),
    "→",
    wpi_master["date"].max().date()
)

print(
    "Missing WPI inflation:",
    wpi_master["wpi_inflation"].isna().sum()
)

print()
print("First 10 observations:")

print(
    wpi_master.head(10).to_string(index=False)
)

print()
print("Latest 15 observations:")

print(
    wpi_master.tail(15).to_string(index=False)
)

print()
print("Output:", OUTPUT_FILE)