import requests
import pandas as pd
import ssl
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager


API_URL = "https://api.mospi.gov.in/api/cpi/getCPIData"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cpi_master.csv"


class LegacySSLAdapter(HTTPAdapter):
    """HTTPS adapter compatible with the MoSPI API server."""

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        context = ssl.create_default_context()

        # Enable legacy TLS renegotiation required by the MoSPI server.
        context.options |= 0x4

        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=context,
            **pool_kwargs
        )


def fetch_cpi(year, month):
    """
    Fetch All India Combined CPI (General)
    for a specific year and month.
    """

    params = {
        "base_year": 2024,
        "year": year,
        "month_code": month,
        "limit": 100,
        "page": 1
    }

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())

    response = session.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if not result.get("data"):
        raise ValueError(
            f"No CPI data returned for {year}-{month:02d}"
        )

    data = pd.DataFrame(result["data"])

    target = data[
        (data["state"] == "All India") &
        (data["sector"] == "Combined") &
        (data["division"] == "CPI (General)")
    ].copy()

    if target.empty:
        raise ValueError(
            f"All India Combined CPI General not found "
            f"for {year}-{month:02d}"
        )

    row = target.iloc[0]

    return {
        "date": pd.Timestamp(
            year=int(row["year"]),
            month=month,
            day=1
        ),
        "year": int(row["year"]),
        "month": pd.Timestamp(
            year=int(row["year"]),
            month=month,
            day=1
        ).strftime("%B"),
        "cpi_index": float(row["index"]),
        "inflation": float(row["inflation"])
    }


def update_cpi_master(year, month):
    """Fetch CPI data and update the master dataset."""

    if OUTPUT_FILE.exists():
        master = pd.read_csv(OUTPUT_FILE)

        master["date"] = pd.to_datetime(
            master["date"]
        )

        # Normalize existing month values.
        master["month"] = master["date"].dt.strftime("%B")

    else:
        master = pd.DataFrame()

    # Fetch new CPI observation.
    new_record = fetch_cpi(year, month)

    new_row = pd.DataFrame([new_record])

    if not master.empty:

        # Replace the same month if it already exists.
        master = master[
            master["date"] != new_record["date"]
        ]

        master = pd.concat(
            [master, new_row],
            ignore_index=True
        )

    else:
        master = new_row

    master = master.sort_values(
        "date"
    ).reset_index(drop=True)

    master.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return new_record


def get_latest_date():
    """Return the latest date currently available in the master dataset."""

    if not OUTPUT_FILE.exists():
        return None

    df = pd.read_csv(OUTPUT_FILE)

    if df.empty:
        return None

    return pd.to_datetime(df["date"]).max()


def get_next_month(date):
    """Return the year and month following a given date."""

    next_date = pd.Timestamp(date) + pd.DateOffset(months=1)

    return next_date.year, next_date.month


if __name__ == "__main__":

    latest_date = get_latest_date()

    if latest_date is None:

        print("No existing CPI master found.")
        print("Please initialize the dataset first.")

    else:

        # ----------------------------------------------------
        # Normalize existing CPI master
        # ----------------------------------------------------

        master = pd.read_csv(
            OUTPUT_FILE
        )

        master["date"] = pd.to_datetime(
            master["date"]
        )

        master["month"] = master["date"].dt.strftime("%B")

        master = master.sort_values(
            "date"
        ).reset_index(drop=True)

        master.to_csv(
            OUTPUT_FILE,
            index=False
        )

        # ----------------------------------------------------
        # Check for next CPI observation
        # ----------------------------------------------------

        print(
            f"Latest CPI in master: "
            f"{latest_date.strftime('%B %Y')}"
        )

        year, month = get_next_month(
            latest_date
        )

        print(
            f"Checking MoSPI API for: "
            f"{pd.Timestamp(year=year, month=month, day=1).strftime('%B %Y')}"
        )

        try:

            record = update_cpi_master(
                year,
                month
            )

            print("\nCPI API Update Successful")
            print("-" * 40)

            print(
                f"Date:       {record['date'].date()}"
            )

            print(
                f"CPI Index:  {record['cpi_index']}"
            )

            print(
                f"Inflation:  {record['inflation']}%"
            )

            print(
                f"Saved to:   {OUTPUT_FILE}"
            )

        except ValueError as e:

            print("\nNo new CPI data available.")
            print(e)

            print(
                f"\nExisting CPI master normalized and saved to:"
            )

            print(
                OUTPUT_FILE
            )