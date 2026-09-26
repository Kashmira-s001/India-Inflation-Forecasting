import pandas as pd
import requests
from pathlib import Path
from io import StringIO


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    PROCESSED_DATA
    / "exchange_rate_master.csv"
)


# ============================================================
# FRED SOURCE
# ============================================================

FRED_URL = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv"
    "?id=EXINUS"
)


# ============================================================
# DOWNLOAD FRED DATA
# ============================================================

def download_exchange_rate():

    print("Downloading latest USD/INR data from FRED...")

    response = requests.get(
        FRED_URL,
        timeout=60
    )

    response.raise_for_status()

    print(
        f"Downloaded {len(response.content):,} bytes."
    )

    return response.text


# ============================================================
# EXTRACT DATA
# ============================================================

def extract_exchange_rate(text):

    print("\nReading FRED data...")

    df = pd.read_csv(
        StringIO(text)
    )

    print("\nFRED columns:")
    print(df.columns.tolist())

    # Rename FRED columns
    df = df.rename(
        columns={
            "observation_date": "date",
            "EXINUS": "usd_inr_rate"
        }
    )

    if "date" not in df.columns:
        raise ValueError(
            "FRED date column was not found."
        )

    if "usd_inr_rate" not in df.columns:
        raise ValueError(
            "EXINUS exchange-rate column was not found."
        )

    # Clean
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["usd_inr_rate"] = pd.to_numeric(
        df["usd_inr_rate"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "date",
            "usd_inr_rate"
        ]
    )

    return df[
        [
            "date",
            "usd_inr_rate"
        ]
    ]


# ============================================================
# BUILD MONTHLY DATASET
# ============================================================

def build_monthly_dataset(df):

    df = df[
        df["date"] >= "2013-01-01"
    ].copy()

    df = (
        df
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Month-over-month change
    df["usd_inr_mom_change_pct"] = (
        df["usd_inr_rate"]
        .pct_change()
        * 100
    )

    # Year-over-year change
    df["usd_inr_yoy_change_pct"] = (
        df["usd_inr_rate"]
        .pct_change(periods=12)
        * 100
    )

    return df[
        [
            "date",
            "usd_inr_rate",
            "usd_inr_mom_change_pct",
            "usd_inr_yoy_change_pct"
        ]
    ]


# ============================================================
# SAVE DATASET
# ============================================================

def save_dataset(df):

    PROCESSED_DATA.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("USD/INR EXCHANGE RATE MASTER DATASET UPDATED")
    print("=" * 60)

    print(
        "Rows:",
        len(df)
    )

    print(
        "Date range:",
        df["date"].min().date(),
        "->",
        df["date"].max().date()
    )

    print("\nLatest observations:")

    print(
        df.tail(3).to_string(
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

    raw_text = (
        download_exchange_rate()
    )

    df = (
        extract_exchange_rate(
            raw_text
        )
    )

    df = (
        build_monthly_dataset(
            df
        )
    )

    save_dataset(df)