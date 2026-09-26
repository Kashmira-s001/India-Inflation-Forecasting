import requests
import pandas as pd
from io import BytesIO
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    PROCESSED_DATA
    / "crude_oil_master.csv"
)


# ============================================================
# WORLD BANK SOURCE
# ============================================================

WORLD_BANK_URL = (
    "https://thedocs.worldbank.org/en/doc/"
    "74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/"
    "related/CMO-Historical-Data-Monthly.xlsx"
)


# ============================================================
# DOWNLOAD WORLD BANK DATA
# ============================================================

def download_world_bank_data():

    print("Downloading latest World Bank commodity data...")

    response = requests.get(
        WORLD_BANK_URL,
        timeout=60
    )

    response.raise_for_status()

    print(
        f"Downloaded {len(response.content):,} bytes."
    )

    return BytesIO(response.content)


# ============================================================
# EXTRACT BRENT CRUDE OIL
# ============================================================

def extract_brent_data(file_object):

    print("\nReading World Bank workbook...")

    raw = pd.read_excel(
        file_object,
        sheet_name="Monthly Prices",
        header=4
    )

    print(
        "Crude oil columns found:"
    )

    print(
        [
            col
            for col in raw.columns
            if "Crude oil" in str(col)
        ]
    )

    # --------------------------------------------------------
    # Select date + Brent
    # --------------------------------------------------------

    crude = raw[
        [
            raw.columns[0],
            "Crude oil, Brent"
        ]
    ].copy()

    crude.columns = [
        "raw_date",
        "brent_price_usd"
    ]

    # --------------------------------------------------------
    # Clean date
    # --------------------------------------------------------

    crude = crude.dropna(
        subset=["raw_date"]
    )

    crude["date"] = pd.to_datetime(
        crude["raw_date"].astype(str),
        format="%YM%m",
        errors="coerce"
    )

    # --------------------------------------------------------
    # Clean price
    # --------------------------------------------------------

    crude["brent_price_usd"] = pd.to_numeric(
        crude["brent_price_usd"],
        errors="coerce"
    )

    crude = crude.dropna(
        subset=[
            "date",
            "brent_price_usd"
        ]
    )

    # --------------------------------------------------------
    # Keep project period
    # --------------------------------------------------------

    crude = crude[
        crude["date"] >= "2013-01-01"
    ].copy()

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    crude = (
        crude
        .sort_values("date")
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Create change features
    # --------------------------------------------------------

    crude["brent_mom_change_pct"] = (
        crude["brent_price_usd"]
        .pct_change()
        * 100
    )

    crude["brent_yoy_change_pct"] = (
        crude["brent_price_usd"]
        .pct_change(periods=12)
        * 100
    )

    return crude[
        [
            "date",
            "brent_price_usd",
            "brent_mom_change_pct",
            "brent_yoy_change_pct"
        ]
    ]


# ============================================================
# SAVE DATASET
# ============================================================

def save_dataset(crude):

    PROCESSED_DATA.mkdir(
        parents=True,
        exist_ok=True
    )

    crude.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("BRENT CRUDE OIL MASTER DATASET UPDATED")
    print("=" * 60)

    print(
        "Rows:",
        len(crude)
    )

    print(
        "Date range:",
        crude["date"].min().date(),
        "->",
        crude["date"].max().date()
    )

    print(
        "Latest observation:"
    )

    print(
        crude.tail(3).to_string(
            index=False
        )
    )

    print(
        "\nOutput:",
        OUTPUT_FILE
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    workbook = (
        download_world_bank_data()
    )

    crude = (
        extract_brent_data(workbook)
    )

    save_dataset(crude)