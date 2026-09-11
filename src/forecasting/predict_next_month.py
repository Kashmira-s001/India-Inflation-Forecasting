import pandas as pd
import joblib
from pathlib import Path

from src.features.build_features import (
    build_features,
    FINAL_FEATURES
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


# --------------------------------------------------
# Load data
# --------------------------------------------------

print("Loading latest economic data...")

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# --------------------------------------------------
# Build features
# --------------------------------------------------

df = build_features(df)


# --------------------------------------------------
# Find latest valid observation
# --------------------------------------------------

latest_data = (
    df.dropna(subset=FINAL_FEATURES)
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
# Generate forecast
# --------------------------------------------------

prediction = model.predict(X_future)[0]


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\n" + "=" * 50)
print("INDIA CPI INFLATION FORECAST")
print("=" * 50)

print(
    f"Latest available month : "
    f"{latest_date.strftime('%B %Y')}"
)

print(
    f"Forecast month         : "
    f"{forecast_date.strftime('%B %Y')}"
)

print(
    f"Predicted inflation    : "
    f"{prediction:.2f}%"
)

print(
    f"Model                  : "
    f"Linear Regression"
)

print("=" * 50)