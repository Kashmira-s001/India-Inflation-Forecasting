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
# Load actual inflation data
# --------------------------------------------------

print("Loading actual inflation data...")

actual_df = pd.read_csv(DATA_PATH)

actual_df["date"] = pd.to_datetime(
    actual_df["date"]
)


# --------------------------------------------------
# Select actual inflation
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
# Calculate forecast errors
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


# --------------------------------------------------
# Keep only forecasts with actual values
# --------------------------------------------------

completed = evaluation_df.dropna(
    subset=["actual_inflation"]
).copy()


# --------------------------------------------------
# Display evaluation
# --------------------------------------------------

print("\n" + "=" * 65)
print("INFLATION FORECAST EVALUATION")
print("=" * 65)


if len(completed) == 0:

    print(
        "\nNo actual inflation values are available "
        "for the stored forecasts yet."
    )

else:

    # Overall metrics
    mae = completed["absolute_error"].mean()

    rmse = np.sqrt(
        completed["squared_error"].mean()
    )

    print(
        f"\nCompleted forecasts : {len(completed)}"
    )

    print(
        f"MAE                 : {mae:.4f}"
    )

    print(
        f"RMSE                : {rmse:.4f}"
    )

    print("\nForecast details:")
    print("-" * 65)

    for _, row in completed.iterrows():

        print(
            f"{row['forecast_date'].strftime('%B %Y')}"
        )

        print(
            f"  Predicted : "
            f"{row['predicted_inflation']:.2f}%"
        )

        print(
            f"  Actual    : "
            f"{row['actual_inflation']:.2f}%"
        )

        print(
            f"  Error     : "
            f"{row['error']:+.2f} percentage points"
        )

        print()


print("=" * 65)