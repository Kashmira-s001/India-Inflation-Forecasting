import pandas as pd


# Final features selected during model evaluation
FINAL_FEATURES = [
    "inflation",
    "inflation_lag_1",
    "inflation_lag_12",
    "wpi_inflation"
]


def build_features(df):
    """
    Create features required for the next-month
    CPI inflation forecasting model.
    """

    df = df.copy()

    # Ensure chronological order
    df = df.sort_values("date").reset_index(drop=True)

    # Create inflation lags
    df["inflation_lag_1"] = (
        df["inflation"].shift(1)
    )

    df["inflation_lag_12"] = (
        df["inflation"].shift(12)
    )

    # Create next-month target
    df["target_next_month_inflation"] = (
        df["inflation"].shift(-1)
    )

    return df


def get_model_data(df):
    """
    Return clean data containing the final model
    features and next-month target.
    """

    df = build_features(df)

    model_df = df.dropna(
        subset=FINAL_FEATURES + [
            "target_next_month_inflation"
        ]
    ).copy()

    X = model_df[FINAL_FEATURES]
    y = model_df["target_next_month_inflation"]

    return X, y, model_df


if __name__ == "__main__":

    print("Feature engineering module loaded.")

    print("\nFinal model features:")
    for feature in FINAL_FEATURES:
        print(f"  - {feature}")