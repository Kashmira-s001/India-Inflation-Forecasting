import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import joblib
from pathlib import Path

from src.features.build_features import (
    build_features,
    FINAL_FEATURES
)

from src.monitoring.shock_detection import (
    detect_shocks
)


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

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_inflation_model.pkl"
)

HISTORY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecast_history.csv"
)


# --------------------------------------------------
# Load economic data
# --------------------------------------------------

print("Loading economic data...")

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)


# --------------------------------------------------
# Build forecasting features
# --------------------------------------------------

df = build_features(df)


# --------------------------------------------------
# Find latest valid observation
# --------------------------------------------------

latest_data = (
    df
    .dropna(subset=FINAL_FEATURES)
    .iloc[-1]
)

latest_date = latest_data["date"]


# --------------------------------------------------
# Determine forecast month
# --------------------------------------------------

forecast_date = (
    latest_date
    + pd.DateOffset(months=1)
)


# --------------------------------------------------
# Prepare model input
# --------------------------------------------------

X_future = pd.DataFrame(
    [[latest_data[feature] for feature in FINAL_FEATURES]],
    columns=FINAL_FEATURES
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

print("Loading trained model...")

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# Generate inflation forecast
# --------------------------------------------------

prediction = model.predict(X_future)[0]


# --------------------------------------------------
# Run shock detection
# --------------------------------------------------

print("Running shock detection...")

shock_df = detect_shocks(df)

latest_shock = shock_df.iloc[-1]


# --------------------------------------------------
# Extract shock signals
# --------------------------------------------------

inflation_shock = bool(
    latest_shock["inflation_shock"]
)

wpi_shock = bool(
    latest_shock["wpi_shock"]
)

brent_shock = bool(
    latest_shock["brent_oil_shock"]
)

usd_inr_shock = bool(
    latest_shock["usd_inr_shock"]
)

overall_shock = bool(
    latest_shock["overall_shock"]
)


# --------------------------------------------------
# Create forecast record
# --------------------------------------------------

forecast_record = pd.DataFrame([{
    "forecast_generated": pd.Timestamp.today().normalize(),
    "data_through": latest_date,
    "forecast_date": forecast_date,
    "predicted_inflation": prediction,
    "model": "Linear Regression",
    "inflation_shock": inflation_shock,
    "wpi_shock": wpi_shock,
    "brent_oil_shock": brent_shock,
    "usd_inr_shock": usd_inr_shock,
    "overall_shock": overall_shock
}])


# --------------------------------------------------
# Save forecast history
# --------------------------------------------------

if HISTORY_PATH.exists():

    history = pd.read_csv(
        HISTORY_PATH,
        parse_dates=[
            "forecast_generated",
            "data_through",
            "forecast_date"
        ]
    )

    # Remove an existing forecast for the same
    # forecast month before adding the new one.
    history = history[
        history["forecast_date"]
        != forecast_date
    ]

    history = pd.concat(
        [history, forecast_record],
        ignore_index=True
    )

else:

    history = forecast_record


history = (
    history
    .sort_values("forecast_date")
    .reset_index(drop=True)
)


HISTORY_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

history.to_csv(
    HISTORY_PATH,
    index=False
)


# --------------------------------------------------
# Display final report
# --------------------------------------------------

print("\n" + "=" * 60)
print("INDIA INFLATION FORECAST")
print("=" * 60)

print(
    f"\nLatest available month : "
    f"{latest_date.strftime('%B %Y')}"
)

print(
    f"Forecast month         : "
    f"{forecast_date.strftime('%B %Y')}"
)

print(
    f"\nPredicted CPI inflation: "
    f"{prediction:.2f}%"
)

print(
    f"Model                  : "
    f"Linear Regression"
)

print("\n" + "-" * 60)
print("ECONOMIC EARLY WARNING")
print("-" * 60)

print(
    f"\nInflation shock        : "
    f"{'YES' if inflation_shock else 'No'}"
)

print(
    f"WPI shock              : "
    f"{'YES' if wpi_shock else 'No'}"
)

print(
    f"Brent oil shock        : "
    f"{'YES' if brent_shock else 'No'}"
)

print(
    f"USD/INR shock          : "
    f"{'YES' if usd_inr_shock else 'No'}"
)

print(
    f"\nOverall shock status   : "
    f"{'STRONG SHOCK SIGNAL' if overall_shock else 'No Strong Shock Signal'}"
)

print("\n" + "-" * 60)

print(
    f"Forecast history saved to:\n"
    f"{HISTORY_PATH}"
)

print("=" * 60)