import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression

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

print("Loading economic data...")

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# Feature engineering
# --------------------------------------------------

print("\nBuilding features...")

df = build_features(df)

model_df = df.dropna(
    subset=FINAL_FEATURES + [
        "target_next_month_inflation"
    ]
).copy()


# --------------------------------------------------
# Prepare X and y
# --------------------------------------------------

X = model_df[FINAL_FEATURES]

y = model_df[
    "target_next_month_inflation"
]


print(f"\nTraining observations: {len(X)}")
print(f"Number of features: {len(FINAL_FEATURES)}")

print("\nFeatures used:")
for feature in FINAL_FEATURES:
    print(f"  - {feature}")


# --------------------------------------------------
# Train final model
# --------------------------------------------------

print("\nTraining Linear Regression model...")

model = LinearRegression()

model.fit(X, y)


# --------------------------------------------------
# Save model
# --------------------------------------------------

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(model, MODEL_PATH)


# --------------------------------------------------
# Display model information
# --------------------------------------------------

print("\nModel trained successfully!")

print("\nModel coefficients:")

for feature, coefficient in zip(
    FINAL_FEATURES,
    model.coef_
):
    print(
        f"  {feature}: {coefficient:.6f}"
    )

print(
    f"\nIntercept: {model.intercept_:.6f}"
)

print(
    f"\nModel saved to:\n{MODEL_PATH}"
)