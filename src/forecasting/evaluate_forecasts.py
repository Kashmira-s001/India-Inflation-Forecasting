import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HISTORY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecast_history.csv"
)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_economic_master.csv"
)


# --------------------------------------------------
# Load forecast history
# --------------------------------------------------

print("Loading forecast history...")

forecast_df = pd.read_csv(
    HISTORY_PATH,
    parse_dates=[
        "forecast_generated",
        "data_through",
        "forecast_date"
    ]
)


# --------------------------------------------------
# Remove previously calculated evaluation columns
# --------------------------------------------------

EVALUATION_COLUMNS = [
    "actual_inflation",
    "error",
    "absolute_error",
    "squared_error",
    "percentage_error",
    "evaluated"
]

forecast_df = forecast_df.drop(
    columns=[
        column
        for column in EVALUATION_COLUMNS
        if column in forecast_df.columns
    ]
)


# --------------------------------------------------
# Load actual inflation data
# --------------------------------------------------

print("Loading actual inflation data...")

actual_df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# --------------------------------------------------
# Prepare actual inflation
# --------------------------------------------------

actual_df = actual_df[
    [
        "date",
        "inflation"
    ]
].copy()

actual_df = actual_df.rename(
    columns={
        "date": "forecast_date",
        "inflation": "actual_inflation"
    }
)


# --------------------------------------------------
# Match forecasts with actual values
# --------------------------------------------------

evaluation_df = forecast_df.merge(
    actual_df,
    on="forecast_date",
    how="left"
)


# --------------------------------------------------
# Calculate evaluation metrics
# --------------------------------------------------

evaluation_df["error"] = (
    evaluation_df["predicted_inflation"]
    - evaluation_df["actual_inflation"]
)

evaluation_df["absolute_error"] = (
    evaluation_df["error"].abs()
)

evaluation_df["squared_error"] = (
    evaluation_df["error"] ** 2
)

evaluation_df["percentage_error"] = (
    evaluation_df["error"]
    / evaluation_df["actual_inflation"]
) * 100

evaluation_df["evaluated"] = (
    evaluation_df["actual_inflation"].notna()
)


# --------------------------------------------------
# Sort and save updated history
# --------------------------------------------------

evaluation_df = (
    evaluation_df
    .sort_values("forecast_date")
    .reset_index(drop=True)
)

evaluation_df.to_csv(
    HISTORY_PATH,
    index=False
)


# --------------------------------------------------
# Completed and pending forecasts
# --------------------------------------------------

completed = evaluation_df[
    evaluation_df["evaluated"]
].copy()

pending = evaluation_df[
    ~evaluation_df["evaluated"]
].copy()


# --------------------------------------------------
# Display evaluation
# --------------------------------------------------

print("\n" + "=" * 70)
print("INFLATION FORECAST EVALUATION")
print("=" * 70)

print(
    f"\nTotal forecasts : {len(evaluation_df)}"
)

print(
    f"Completed       : {len(completed)}"
)

print(
    f"Pending         : {len(pending)}"
)


# --------------------------------------------------
# Overall metrics
# --------------------------------------------------

if len(completed) == 0:

    print(
        "\nNo completed forecasts available yet."
    )

else:

    mae = completed["absolute_error"].mean()

    rmse = np.sqrt(
        completed["squared_error"].mean()
    )

    mean_error = completed["error"].mean()

    print(
        f"\nMAE             : "
        f"{mae:.4f} percentage points"
    )

    print(
        f"RMSE            : "
        f"{rmse:.4f} percentage points"
    )

    print(
        f"Mean Error      : "
        f"{mean_error:+.4f} percentage points"
    )


# --------------------------------------------------
# Completed forecast details
# --------------------------------------------------

if len(completed) > 0:

    print("\n" + "-" * 70)
    print("COMPLETED FORECASTS")
    print("-" * 70)

    for _, row in completed.iterrows():

        print(
            f"\n{row['forecast_date'].strftime('%B %Y')}"
        )

        print(
            f"  Predicted : "
            f"{row['predicted_inflation']:.4f}%"
        )

        print(
            f"  Actual    : "
            f"{row['actual_inflation']:.4f}%"
        )

        print(
            f"  Error     : "
            f"{row['error']:+.4f} percentage points"
        )

        print(
            f"  Abs Error : "
            f"{row['absolute_error']:.4f} percentage points"
        )

        print(
            f"  Error %   : "
            f"{row['percentage_error']:+.2f}%"
        )


# --------------------------------------------------
# Pending forecasts
# --------------------------------------------------

if len(pending) > 0:

    print("\n" + "-" * 70)
    print("PENDING FORECASTS")
    print("-" * 70)

    for _, row in pending.iterrows():

        print(
            f"\n{row['forecast_date'].strftime('%B %Y')}"
        )

        print(
            f"  Predicted : "
            f"{row['predicted_inflation']:.4f}%"
        )

        print(
            "  Actual    : Pending"
        )


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("\n" + "=" * 70)

print(
    f"Forecast history updated:\n"
    f"{HISTORY_PATH}"
)

print("=" * 70)