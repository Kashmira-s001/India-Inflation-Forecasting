import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
from pathlib import Path
import re


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DATA / "wpi_master.csv"

OEA_URL = "https://eaindustry.nic.in/download_data_2223.asp"


# ============================================================
# 2. FIND LATEST WPI FILE
# ============================================================

def find_latest_wpi_file():

    print("Checking official OEA WPI page...")

    response = requests.get(
        OEA_URL,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    files = []

    for link in soup.find_all("a", href=True):

        href = link["href"]

        match = re.search(
            r"wpi_monthly_index_(\d{6})\.xlsx",
            href,
            re.IGNORECASE
        )

        if match:

            period = match.group(1)

            files.append(
                (period, href)
            )

    if not files:
        raise ValueError(
            "No WPI monthly Excel file found on OEA website."
        )

    # Latest YYYYMM
    latest_period, latest_href = max(
        files,
        key=lambda x: x[0]
    )

    if latest_href.startswith("http"):
        file_url = latest_href

    else:
        file_url = (
            "https://eaindustry.nic.in/"
            + latest_href.lstrip("/")
        )

    return latest_period, file_url


# ============================================================
# 3. DOWNLOAD WPI WORKBOOK
# ============================================================

def download_wpi_file(file_url):

    print(
        f"Downloading: {file_url}"
    )

    response = requests.get(
        file_url,
        timeout=30
    )

    response.raise_for_status()

    return BytesIO(
        response.content
    )


# ============================================================
# 4. EXTRACT ALL COMMODITIES
# ============================================================

def extract_wpi_data(file_object):

    df = pd.read_excel(
        file_object,
        sheet_name="Sheet3"
    )

    commodity = df[
        df["Commodity Name"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "all commodities"
    ].copy()

    if commodity.empty:
        raise ValueError(
            "All Commodities row not found."
        )

    # Find monthly columns
    month_columns = [
        col
        for col in df.columns
        if re.match(
            r"^[A-Z][a-z]{2}-\d{2}$",
            str(col)
        )
    ]

    records = []

    for month_col in month_columns:

        current_date = pd.to_datetime(
            month_col,
            format="%b-%y"
        )

        current_index = pd.to_numeric(
            commodity.iloc[0][month_col],
            errors="coerce"
        )

        if pd.isna(current_index):
            continue

        # Find same month one year earlier
        previous_col = (
            current_date - pd.DateOffset(years=1)
        ).strftime("%b-%y")

        if previous_col in commodity.columns:

            previous_index = pd.to_numeric(
                commodity.iloc[0][previous_col],
                errors="coerce"
            )

        else:
            previous_index = None

        if (
            previous_index is not None
            and not pd.isna(previous_index)
        ):

            inflation = (
                (current_index - previous_index)
                / previous_index
            ) * 100

        else:

            inflation = None

        records.append({
            "date": current_date,
            "year": current_date.year,
            "month": current_date.strftime("%B"),
            "wpi_index": current_index,
            "wpi_inflation": inflation
        })

    return pd.DataFrame(records)


# ============================================================
# 5. UPDATE MASTER DATASET
# ============================================================

def update_wpi_master(new_data):

    if OUTPUT_FILE.exists():

        master = pd.read_csv(
            OUTPUT_FILE,
            parse_dates=["date"]
        )

    else:

        master = pd.DataFrame()

    if not master.empty:

        master = master[
            ~master["date"].isin(
                new_data["date"]
            )
        ]

    master = pd.concat(
        [master, new_data],
        ignore_index=True
    )

    master = master.sort_values(
        "date"
    ).reset_index(drop=True)

    master.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return master


# ============================================================
# 6. MAIN
# ============================================================

if __name__ == "__main__":

    latest_period, file_url = (
        find_latest_wpi_file()
    )

    print(
        f"Latest WPI file found: "
        f"{latest_period}"
    )

    workbook = download_wpi_file(
        file_url
    )

    wpi_data = extract_wpi_data(
        workbook
    )

    master = update_wpi_master(
        wpi_data
    )

    print("\nWPI master updated")
    print("-" * 40)

    print(
        master.tail(10).to_string(
            index=False
        )
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )