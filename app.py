import streamlit as st

import pandas as pd

import subprocess

import sys

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

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CPI_DATA = PROCESSED_DIR / "cpi_master.csv"
WPI_DATA = PROCESSED_DIR / "wpi_master.csv"
REPO_DATA = PROCESSED_DIR / "repo_rate_master.csv"
CRUDE_DATA = PROCESSED_DIR / "crude_oil_master.csv"
FX_DATA = PROCESSED_DIR / "exchange_rate_master.csv"

PIPELINE_SCRIPT = PROJECT_ROOT / "run_pipeline.py"

# --------------------------------------------------

# Load data

# --------------------------------------------------

def load_source_data(file_path, value_column):
    """Load an indicator's source file and return valid observations."""
    df = pd.read_csv(file_path)

    if "date" not in df.columns or value_column not in df.columns:
        raise ValueError(
            f"{file_path.name} must contain 'date' and '{value_column}' columns."
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[value_column] = pd.to_numeric(df[value_column], errors="coerce")

    return (
        df.dropna(subset=["date", value_column])
        .sort_values("date")
        .reset_index(drop=True)
    )


def get_latest_value(file_path, value_column):
    """Return the latest non-missing value and its observation date."""
    df = load_source_data(file_path, value_column)

    if df.empty:
        return None, None

    latest_row = df.iloc[-1]
    return latest_row[value_column], latest_row["date"]


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

# --------------------------------------------------

# Refresh Data and Forecast

# --------------------------------------------------

if st.session_state.pop("refresh_success", False):

    st.success("Datasets and forecast refreshed successfully!")

# Place the refresh button at the top-right

header_space, refresh_col = st.columns([8, 2])

with refresh_col:

    if st.button(

        "🔄 Refresh Data & Forecast",

        use_container_width=True,

        key="refresh_pipeline_button"

    ):

        if not PIPELINE_SCRIPT.is_file():

            st.error(f"Pipeline not found: {PIPELINE_SCRIPT}")

        else:

            try:

                with st.spinner(

                    "Updating datasets and generating forecast..."

                ):

                    subprocess.run(

                        [sys.executable, str(PIPELINE_SCRIPT)],

                        cwd=str(PROJECT_ROOT),

                        check=True,

                        timeout=900

                    )

                st.cache_data.clear()

                st.session_state["refresh_success"] = True

                st.rerun()

            except subprocess.TimeoutExpired:

                st.error(

                    "Pipeline timed out after 15 minutes. "

                    "Check the terminal for details."

                )

            except subprocess.CalledProcessError as e:

                st.error(

                    f"Pipeline failed with exit code {e.returncode}. "

                    "Check the terminal for the failing step."

                )

            except Exception as e:

                st.error(f"Refresh failed: {e}")

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

st.title("🇮🇳 India Inflation Forecasting & Economic Intelligence")

st.write("A data-driven dashboard for monitoring and forecasting India's CPI inflation.")

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

# --------------------------------------------------
# Economic Indicators
# --------------------------------------------------

st.divider()
st.subheader("Economic Indicators")

indicator_specs = [
    ("WPI Inflation", WPI_DATA, "wpi_inflation", "{:.2f}%"),
    ("Repo Rate", REPO_DATA, "repo_rate", "{:.2f}%"),
    ("Brent Crude", CRUDE_DATA, "brent_price_usd", "${:.2f}"),
    ("USD / INR", FX_DATA, "usd_inr_rate", "₹{:.2f}"),
]

indicator_cols = st.columns(4)

for col, (name, file_path, value_column, value_format) in zip(
    indicator_cols, indicator_specs
):
    with col:
        try:
            value, observation_date = get_latest_value(file_path, value_column)

            if value is None:
                st.metric(name, "N/A")
                st.caption("No available observation")
            else:
                st.metric(name, value_format.format(value))
                st.caption(f"Latest data: {observation_date:%b %Y}")

        except (FileNotFoundError, KeyError, ValueError) as exc:
            st.metric(name, "Unavailable")
            st.caption(f"Check source data: {exc}")


# --------------------------------------------------
# WPI Inflation Trend
# --------------------------------------------------

st.subheader("WPI Inflation Trend")

try:
    wpi_chart = load_source_data(WPI_DATA, "wpi_inflation")
    wpi_chart = wpi_chart.set_index("date")[["wpi_inflation"]]
    st.line_chart(wpi_chart, y="wpi_inflation")
    st.caption(f"Latest WPI observation: {wpi_chart.index.max():%b %Y}")
except (FileNotFoundError, KeyError, ValueError) as exc:
    st.warning(f"Could not load WPI trend: {exc}")


# --------------------------------------------------
# Brent Crude and USD/INR Trends
# --------------------------------------------------

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    st.subheader("Brent Crude Price")
    try:
        brent_chart = load_source_data(CRUDE_DATA, "brent_price_usd")
        brent_chart = brent_chart.set_index("date")[["brent_price_usd"]]
        st.line_chart(brent_chart, y="brent_price_usd")
        st.caption(f"Latest Brent observation: {brent_chart.index.max():%b %Y}")
    except (FileNotFoundError, KeyError, ValueError) as exc:
        st.warning(f"Could not load Brent crude trend: {exc}")

with trend_col2:
    st.subheader("USD / INR Exchange Rate")
    try:
        fx_chart = load_source_data(FX_DATA, "usd_inr_rate")
        fx_chart = fx_chart.set_index("date")[["usd_inr_rate"]]
        st.line_chart(fx_chart, y="usd_inr_rate")
        st.caption(f"Latest exchange-rate observation: {fx_chart.index.max():%b %Y}")
    except (FileNotFoundError, KeyError, ValueError) as exc:
        st.warning(f"Could not load USD/INR trend: {exc}")


# --------------------------------------------------
# Repo Rate Trend
# --------------------------------------------------

st.subheader("RBI Repo Rate Trend")

try:
    repo_chart = load_source_data(REPO_DATA, "repo_rate")
    repo_chart = repo_chart.set_index("date")[["repo_rate"]]
    st.line_chart(repo_chart, y="repo_rate")
    st.caption(f"Latest repo-rate observation: {repo_chart.index.max():%b %Y}")
except (FileNotFoundError, KeyError, ValueError) as exc:
    st.warning(f"Could not load repo-rate trend: {exc}")


# Early Warning Signals

# --------------------------------------------------

st.divider()

st.subheader("Early Warning Signals")

latest_forecast = (

    forecast_df

    .sort_values("forecast_date")

    .iloc[-1]

)

# Build the repo-rate warning from the latest two observations in the
# standalone source file, so it is not limited by the CPI master timeline.
repo_rate_changed = False
try:
    repo_warning_data = load_source_data(REPO_DATA, "repo_rate")
    if len(repo_warning_data) >= 2:
        repo_warning_data = repo_warning_data.sort_values("date")
        latest_repo_rate = float(repo_warning_data.iloc[-1]["repo_rate"])
        previous_repo_rate = float(repo_warning_data.iloc[-2]["repo_rate"])
        repo_rate_changed = latest_repo_rate != previous_repo_rate
except (FileNotFoundError, KeyError, ValueError, IndexError):
    # If source data is unavailable, use the saved signal if present.
    if "repo_rate_shock" in forecast_df.columns:
        repo_rate_changed = bool(latest_forecast["repo_rate_shock"])

signals = {
    "Inflation Shock": latest_forecast["inflation_shock"],
    "WPI Shock": latest_forecast["wpi_shock"],
    "Brent Oil Shock": latest_forecast["brent_oil_shock"],
    "USD/INR Shock": latest_forecast["usd_inr_shock"],
    "Repo Rate Change": repo_rate_changed,
}

cols = st.columns(len(signals))

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
