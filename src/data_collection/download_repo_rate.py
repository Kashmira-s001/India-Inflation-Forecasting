import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DATA / "repo_rate_master.csv"

RBI_URL = "https://www.rbi.org.in/"


# ============================================================
# 2. FETCH CURRENT RBI REPO RATE
# ============================================================

def fetch_current_repo_rate():

    print("Fetching current repo rate from RBI...")

    response = requests.get(
        RBI_URL,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"Policy Repo Rate\s*:\s*([0-9]+(?:\.[0-9]+)?)%",
        text
    )

    if not match:
        raise ValueError(
            "Policy Repo Rate could not be found on RBI website."
        )

    repo_rate = float(match.group(1))

    return repo_rate


# ============================================================
# 3. UPDATE REPO MASTER
# ============================================================

def update_repo_master(repo_rate):

    if OUTPUT_FILE.exists():

        df = pd.read_csv(
            OUTPUT_FILE,
            parse_dates=["date"]
        )

    else:

        df = pd.DataFrame(
            columns=[
                "date",
                "repo_rate"
            ]
        )

    current_month = pd.Timestamp.today().to_period("M").to_timestamp()

    # Add/update the current month's observed RBI rate
    new_row = pd.DataFrame({
        "date": [current_month],
        "repo_rate": [repo_rate]
    })

    df = df[df["date"] != current_month]

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    # Create a continuous monthly timeline
    start_date = df["date"].min()

    monthly_dates = pd.date_range(
        start=start_date,
        end=current_month,
        freq="MS"
    )

    df = (
        df.set_index("date")
        .reindex(monthly_dates)
        .rename_axis("date")
        .reset_index()
    )

    # Carry the last known RBI policy rate forward
    df["repo_rate"] = df["repo_rate"].ffill()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return df


# ============================================================
# 4. MAIN
# ============================================================

if __name__ == "__main__":

    repo_rate = fetch_current_repo_rate()

    print(
        f"Current RBI Policy Repo Rate: {repo_rate:.2f}%"
    )

    repo_master = update_repo_master(
        repo_rate
    )

    print(
        f"\nUpdated repo-rate master:"
    )

    print(
        repo_master.tail(10).to_string(
            index=False
        )
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )