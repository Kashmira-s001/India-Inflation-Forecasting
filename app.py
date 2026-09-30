import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="India Inflation Forecasting",
    page_icon="🇮🇳",
    layout="wide"
)

# --------------------------------------------------
# File paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

ECONOMIC_DATA = PROJECT_ROOT / "data" / "processed" / "final_economic_master.csv"
FORECAST_DATA = PROJECT_ROOT / "data" / "processed" / "forecast_history.csv"


# --------------------------------------------------
# Load data
# --------------------------------------------------

economic_df = pd.read_csv(ECONOMIC_DATA)
forecast_df = pd.read_csv(FORECAST_DATA)

economic_df["date"] = pd.to_datetime(economic_df["date"])
forecast_df["forecast_date"] = pd.to_datetime(forecast_df["forecast_date"])


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🇮🇳 Inflation Monitor")

    st.markdown(
        """
        ### About

        This dashboard monitors India's CPI inflation
        and generates a one-month-ahead inflation forecast.

        ### Forecasting Approach

        **Target:** CPI inflation

        **Horizon:** 1 month ahead

        **Model:** Linear Regression

        ### Key Indicators

        - CPI inflation
        - WPI inflation
        - RBI repo rate
        - Brent crude oil
        - USD/INR exchange rate

        ### Data

        Economic data is processed through the
        project's automated Python pipeline.
        """
    )

    st.divider()

    st.caption(
        "India Inflation Forecasting & Economic Intelligence"
    )

# --------------------------------------------------
# Training observations
# --------------------------------------------------

training_observations = economic_df.copy()

training_observations["inflation_lag_1"] = (
    training_observations["inflation"].shift(1)
)

training_observations["inflation_lag_12"] = (
    training_observations["inflation"].shift(12)
)

training_observations["target_next_month_inflation"] = (
    training_observations["inflation"].shift(-1)
)

training_observations = training_observations.dropna(
    subset=[
        "inflation",
        "inflation_lag_1",
        "inflation_lag_12",
        "wpi_inflation",
        "target_next_month_inflation"
    ]
)

training_observations_count = len(training_observations)

# --------------------------------------------------
# Latest actual inflation
# --------------------------------------------------

latest_actual = (
    economic_df
    .dropna(subset=["inflation"])
    .sort_values("date")
    .iloc[-1]
)

current_inflation = latest_actual["inflation"]
data_through = latest_actual["date"]

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <style>
    .dashboard-header {
        text-align: center;
        margin-bottom: 10px;
    }

    .dashboard-header h1 {
        font-size: 42px;
        margin-bottom: 10px;
    }

    .dashboard-header p {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="dashboard-header">
        <h1>🇮🇳 India Inflation Forecasting & Economic Intelligence</h1>
        <p>A data-driven dashboard for monitoring and forecasting India's CPI inflation.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Latest forecast
# --------------------------------------------------

latest_forecast = (
    forecast_df
    .sort_values("forecast_date")
    .iloc[-1]
)

next_month_forecast = latest_forecast["predicted_inflation"]
forecast_month = latest_forecast["forecast_date"]


# --------------------------------------------------
# Latest evaluated forecast
# --------------------------------------------------

evaluated_forecasts = forecast_df.dropna(
    subset=["actual_inflation", "error"]
)

if not evaluated_forecasts.empty:
    latest_evaluated = (
        evaluated_forecasts
        .sort_values("forecast_date")
        .iloc[-1]
    )

    latest_error = latest_evaluated["error"]
    error_month = latest_evaluated["forecast_date"]

    forecast_error_display = f"{latest_error:.2f} pp"
    error_label = (
        f"Latest Forecast Error "
        f"({error_month.strftime('%b %Y')})"
    )
else:
    forecast_error_display = "N/A"
    error_label = "Latest Forecast Error"


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Inflation",
        f"{current_inflation:.2f}%"
    )

with col2:
    st.metric(
        f"Forecast for {forecast_month.strftime('%B %Y')}",
        f"{next_month_forecast:.2f}%"
    )

with col3:
    st.metric(
        "Data Through",
        data_through.strftime("%b %Y")
    )

with col4:
    st.metric(
        error_label,
        forecast_error_display
    )

# --------------------------------------------------
# Inflation Trend
# --------------------------------------------------

st.divider()
st.subheader("India CPI Inflation Trend")

inflation_chart = (
    economic_df[
        ["date", "inflation"]
    ]
    .dropna()
    .set_index("date")
)

st.line_chart(
    inflation_chart,
    y="inflation"
)

# --------------------------------------------------
# Forecast vs Actual
# --------------------------------------------------

st.divider()
st.subheader("Forecast vs Actual Inflation")

forecast_plot = forecast_df.copy()

forecast_plot = forecast_plot.dropna(
    subset=["actual_inflation"]
)

forecast_plot = forecast_plot[
    ["forecast_date", "predicted_inflation", "actual_inflation"]
].copy()

forecast_plot["forecast_date"] = (
    forecast_plot["forecast_date"]
    .dt.strftime("%b %Y")
)

forecast_plot = forecast_plot.rename(
    columns={
        "predicted_inflation": "Forecast",
        "actual_inflation": "Actual"
    }
)

if len(forecast_plot) == 1:

    comparison = forecast_plot.iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Forecast",
            f"{comparison['Forecast']:.2f}%"
        )

    with col2:
        st.metric(
            "Actual",
            f"{comparison['Actual']:.2f}%"
        )

    difference = comparison["Forecast"] - comparison["Actual"]

    st.caption(
        f"Forecast error: {difference:.2f} percentage points"
    )

else:

    chart_data = forecast_plot.set_index("forecast_date")

    st.line_chart(chart_data)

# --------------------------------------------------
# Economic Indicators
# --------------------------------------------------

st.divider()

st.subheader("Economic Indicators")

latest = economic_df.sort_values("date").iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "WPI Inflation",
        f"{latest['wpi_inflation']:.2f}%"
    )

with col2:
    st.metric(
        "Repo Rate",
        f"{latest['repo_rate']:.2f}%"
    )

with col3:
    st.metric(
        "Brent Crude",
        f"${latest['brent_price_usd']:.2f}"
    )

with col4:
    st.metric(
        "USD / INR",
        f"₹{latest['usd_inr_rate']:.2f}"
    )

# --------------------------------------------------
# WPI Inflation Trend
# --------------------------------------------------

st.subheader("WPI Inflation Trend")

wpi_chart = (
    economic_df[
        ["date", "wpi_inflation"]
    ]
    .dropna()
    .set_index("date")
)

st.line_chart(
    wpi_chart,
    y="wpi_inflation"
)

# --------------------------------------------------
# Brent Crude and USD/INR Trends
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Brent Crude Price")

    brent_chart = (
        economic_df[
            ["date", "brent_price_usd"]
        ]
        .dropna()
        .set_index("date")
    )

    st.line_chart(
        brent_chart,
        y="brent_price_usd"
    )

with col2:
    st.subheader("USD / INR Exchange Rate")

    fx_chart = (
        economic_df[
            ["date", "usd_inr_rate"]
        ]
        .dropna()
        .set_index("date")
    )

    st.line_chart(
        fx_chart,
        y="usd_inr_rate"
    )

# --------------------------------------------------
# Repo Rate Trend
# --------------------------------------------------

st.subheader("RBI Repo Rate Trend")

repo_chart = (
    economic_df[
        ["date", "repo_rate"]
    ]
    .dropna()
    .set_index("date")
)

st.line_chart(
    repo_chart,
    y="repo_rate"
)

# --------------------------------------------------
# Early Warning Signals
# --------------------------------------------------

st.divider()

st.subheader("Early Warning Signals")

latest_forecast = (
    forecast_df
    .sort_values("forecast_date")
    .iloc[-1]
)

signals = {
    "Inflation Shock": latest_forecast["inflation_shock"],
    "WPI Shock": latest_forecast["wpi_shock"],
    "Brent Oil Shock": latest_forecast["brent_oil_shock"],
    "USD/INR Shock": latest_forecast["usd_inr_shock"],
    "Overall Shock": latest_forecast["overall_shock"],
}

cols = st.columns(5)

for col, (name, status) in zip(cols, signals.items()):
    with col:
        if bool(status):
            st.error(f"⚠️ {name}\n\nDetected")
        else:
            st.success(f"✓ {name}\n\nNormal")

# --------------------------------------------------
# Model Information
# --------------------------------------------------

st.divider()

st.subheader("Model Information")

st.markdown(
    """
    <style>
    .model-info-label {
        font-size: 14px;
        color: #555;
        margin-bottom: 2px;
    }

    .model-info-value {
        font-size: 24px;
        font-weight: 500;
        color: #1f2937;
    }
    </style>
    """,
    unsafe_allow_html=True
)

model_col1, model_col2, model_col3, model_col4 = st.columns(4)

with model_col1:
    st.markdown('<div class="model-info-label">Model</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="model-info-value">{latest_forecast["model"]}</div>',
        unsafe_allow_html=True
    )

with model_col2:
    st.markdown('<div class="model-info-label">Forecast Horizon</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="model-info-value">1 Month</div>',
        unsafe_allow_html=True
    )

with model_col3:
    st.markdown('<div class="model-info-label">Training Observations</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="model-info-value">{training_observations_count}</div>',
        unsafe_allow_html=True
    )

with model_col4:
    st.markdown(
        '<div class="model-info-label">Training Period</div>',
        unsafe_allow_html=True
    )

    training_start = training_observations["date"].min()
    training_end = training_observations["date"].max()

    training_period = (
        f"{training_start.strftime('%b %Y')} – "
        f"{training_end.strftime('%b %Y')}"
    )

    st.markdown(
        f'<div class="model-info-value">{training_period}</div>',
        unsafe_allow_html=True
    )