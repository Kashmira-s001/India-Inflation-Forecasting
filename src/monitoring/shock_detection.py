import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_economic_master.csv"
)


# --------------------------------------------------
# Shock detection settings
# --------------------------------------------------

LOOKBACK_MONTHS = 12
SHOCK_THRESHOLD = 2.0


# --------------------------------------------------
# Detect economic shocks
# --------------------------------------------------

def detect_shocks(df):
    """
    Detect unusually large month-to-month movements
    in important inflation-related economic variables.
    """

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = (
        df
        .sort_values("date")
        .reset_index(drop=True)
    )

    # --------------------------------------------------
    # Calculate monthly changes
    # --------------------------------------------------

    df["inflation_change"] = (
        df["inflation"].diff()
    )

    df["wpi_change"] = (
        df["wpi_inflation"].diff()
    )

    df["brent_change"] = (
        df["brent_mom_change_pct"]
    )

    df["usd_inr_change"] = (
        df["usd_inr_mom_change_pct"]
    )

    # --------------------------------------------------
    # Variables to monitor
    # --------------------------------------------------

    shock_variables = {
        "inflation": "inflation_change",
        "wpi": "wpi_change",
        "brent_oil": "brent_change",
        "usd_inr": "usd_inr_change"
    }

    # --------------------------------------------------
    # Calculate rolling historical statistics
    # --------------------------------------------------

    for name, column in shock_variables.items():

        rolling_mean = (
            df[column]
            .rolling(LOOKBACK_MONTHS)
            .mean()
            .shift(1)
        )

        rolling_std = (
            df[column]
            .rolling(LOOKBACK_MONTHS)
            .std()
            .shift(1)
        )

        df[f"{name}_zscore"] = (
            (df[column] - rolling_mean)
            / rolling_std
        )

        df[f"{name}_shock"] = (
            df[f"{name}_zscore"].abs()
            >= SHOCK_THRESHOLD
        )

    # --------------------------------------------------
    # Overall shock flag
    # --------------------------------------------------

    shock_columns = [
        "inflation_shock",
        "wpi_shock",
        "brent_oil_shock",
        "usd_inr_shock"
    ]

    df["overall_shock"] = (
        df[shock_columns]
        .any(axis=1)
    )

    return df


# --------------------------------------------------
# Latest shock report
# --------------------------------------------------

def get_latest_shock_report(df):

    latest = df.iloc[-1]

    report = {
        "date": latest["date"],
        "inflation_zscore": latest["inflation_zscore"],
        "wpi_zscore": latest["wpi_zscore"],
        "brent_oil_zscore": latest["brent_oil_zscore"],
        "usd_inr_zscore": latest["usd_inr_zscore"],
        "overall_shock": latest["overall_shock"]
    }

    return report


# --------------------------------------------------
# Run directly
# --------------------------------------------------

if __name__ == "__main__":

    print("Loading economic data...")

    df = pd.read_csv(DATA_PATH)

    print("Running shock detection...")

    shock_df = detect_shocks(df)

    report = get_latest_shock_report(shock_df)

    print("\n" + "=" * 55)
    print("ECONOMIC SHOCK DETECTION")
    print("=" * 55)

    print(
        f"Latest month: "
        f"{report['date'].strftime('%B %Y')}"
    )

    print("\nZ-Scores:")

    print(
        f"  Inflation : "
        f"{report['inflation_zscore']:.2f}"
    )

    print(
        f"  WPI      : "
        f"{report['wpi_zscore']:.2f}"
    )

    print(
        f"  Brent Oil: "
        f"{report['brent_oil_zscore']:.2f}"
    )

    print(
        f"  USD/INR  : "
        f"{report['usd_inr_zscore']:.2f}"
    )

    print("\nShock threshold:")
    print(f"  |Z| >= {SHOCK_THRESHOLD}")

    if report["overall_shock"]:
        print("\n⚠️ STRONG ECONOMIC SHOCK SIGNAL")
    else:
        print("\n✅ NO STRONG SHOCK SIGNAL")

    print("=" * 55)