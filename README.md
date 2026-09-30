# 🇮🇳 India Inflation Forecasting & Economic Intelligence System

A data-driven forecasting system for predicting **India's next-month CPI inflation** using historical inflation patterns and selected macroeconomic indicators.

The project is designed as an **ongoing monthly forecasting pipeline**, not a one-time machine learning experiment. As new economic data becomes available, the system can update the economic dataset, retrain the model, generate a new forecast, store the prediction, and later evaluate it against the official actual inflation value.

---

## 🌐 Live Dashboard

👉 **[Open the Live Streamlit Dashboard](https://india-inflation-forecasting.streamlit.app/)**

The dashboard provides the latest CPI inflation, next-month forecast, economic indicators, forecast evaluation, and early-warning signals.

---

## 📌 Overview

Inflation is influenced by domestic price movements as well as broader economic conditions such as wholesale prices, monetary policy, crude oil prices, and exchange rates.

This project explores whether these signals can help forecast India's **Consumer Price Index (CPI) inflation one month ahead**.

The system brings together:

- Historical CPI inflation
- WPI inflation
- RBI repo rate
- Brent crude oil prices
- USD/INR exchange rate
- Food & Beverages CPI data
- Time-series feature engineering
- Machine learning model evaluation
- Economic shock detection
- Forecast history and evaluation
- Interactive Streamlit dashboard

The goal is to build a **transparent, reproducible, interpretable, and continuously updateable forecasting workflow**.

---

# 🎯 Objective

The primary forecasting objective is:

> **Using information available up to month `t`, forecast India's CPI inflation for month `t + 1`.**

For example:

```text
August 2026 Economic Data
          │
          ▼
   Feature Engineering
          │
          ▼
    Forecasting Model
          │
          ▼
September 2026 CPI Inflation
```

When the next month's official data becomes available, it becomes part of the historical dataset and can be used to generate the following month's forecast.

For example:

```text
July Data
   ↓
Forecast August

August Data
   ↓
Forecast September

September Data
   ↓
Forecast October

        ...
```

An important design principle is that **actual observed inflation is used when it becomes available**. A previous forecast is not treated as the actual economic observation.

---

# 📊 Data

The project works with monthly economic data beginning in **2013**, with the final modelling dataset extending through the latest available observations.

The main indicators are:

| Indicator | Role in the Project |
|---|---|
| CPI Inflation | Primary forecasting target |
| WPI Inflation | Indicator of wholesale price pressure |
| RBI Repo Rate | Monetary policy indicator |
| Brent Crude Oil | Energy and global commodity price indicator |
| USD/INR Exchange Rate | Currency and imported-price pressure indicator |
| Food & Beverages CPI | Food-related price analysis |

Processed datasets are stored under:

```text
data/processed/
```

Raw source files are intentionally excluded from the public GitHub repository.

Detailed source, coverage, transformation, and usage information is documented in:

```text
data/metadata/data_sources.md
```

---

# 🛠️ Data Sources

The project uses official and publicly available economic data sources.

Major sources include:

- Ministry of Statistics and Programme Implementation (MoSPI)
- e-Sankhyiki
- Reserve Bank of India (RBI)
- Office of Economic Adviser (WPI)
- World Bank Commodity Markets
- Federal Reserve Economic Data (FRED) for the USD/INR series

The exact source and processing details for each dataset are documented in:

```text
data/metadata/data_sources.md
```

---

# 🧹 Data Processing Pipeline

The project processes each economic indicator separately before combining them into the final modelling dataset.

```text
Official / Public Economic Data
             │
             ▼
       Data Collection
             │
             ▼
      Cleaning & Validation
             │
             ▼
       Monthly Alignment
             │
             ▼
     Individual Master Data
             │
             ▼
      Economic Master Data
             │
             ▼
   Enriched Economic Master
             │
             ▼
     Feature Engineering
             │
             ▼
       Forecasting Model
             │
             ▼
       Next-Month Forecast
             │
             ▼
      Forecast Evaluation
```

The complete workflow can be executed using:

```bash
python run_pipeline.py
```

The pipeline updates the available data sources, rebuilds the economic datasets, evaluates previous forecasts, retrains the model, and generates the next-month forecast.

---

# 🧠 Feature Engineering

The forecasting problem is formulated as a **one-step-ahead time-series prediction problem**.

The target variable is:

```text
target_next_month_inflation
```

It represents the CPI inflation value in the following month.

The final forecasting model uses four features:

```text
inflation
inflation_lag_1
inflation_lag_12
wpi_inflation
```

### Feature descriptions

| Feature | Description |
|---|---|
| `inflation` | Current CPI inflation |
| `inflation_lag_1` | CPI inflation from the previous month |
| `inflation_lag_12` | CPI inflation from the same month one year earlier |
| `wpi_inflation` | Current WPI inflation |

The lag features allow the model to capture **recent inflation momentum** and **year-over-year historical patterns**.

Although repo rate, Brent crude oil, USD/INR, and Food & Beverages data are included in the broader economic intelligence system, they are currently used primarily for economic monitoring and shock detection rather than as direct inputs to the final four-feature forecasting model.

---

# 🤖 Models Evaluated

Several approaches were evaluated during model development.

### Machine Learning Models

- Linear Regression
- Ridge Regression
- Random Forest
- XGBoost

### Statistical Time-Series Models

- ARIMA
- SARIMA

### Baseline

- Naive persistence forecast

The naive baseline is important because inflation is a persistent time series. A forecasting model should therefore be evaluated against the simple assumption that the next month's inflation will remain close to the current value.

---

# 📈 Model Selection

The final production model is:

## Linear Regression

using:

```text
inflation
inflation_lag_1
inflation_lag_12
wpi_inflation
```

The final model was selected based primarily on **Mean Absolute Error (MAE)** during walk-forward validation, while the naive model is retained as a benchmark.

The model is intentionally simple because the dataset contains a relatively small number of monthly observations. The project prioritizes:

- Interpretability
- Reproducibility
- Stability
- Simple monthly retraining
- Transparent evaluation

The project does **not** claim that Linear Regression universally outperforms all alternative models.

---

# 🧪 Model Validation

Because this is a time-series problem, random train-test splitting was avoided.

The project uses chronological evaluation and walk-forward validation.

### 1. Chronological Validation

Historical observations are separated chronologically rather than randomly.

```text
Past Data ─────────────────────► Future Data
     Train                           Test
```

### 2. Walk-Forward Validation

The model is repeatedly trained using information available up to a particular point and then used to forecast the next observation.

```text
Train
  │
  └──► Predict next month

Train + New Observation
  │
  └──► Predict next month

Train + More Observations
  │
  └──► Predict next month

             ...
```

This better represents how the model operates in a real monthly forecasting environment.

---

# 📊 Final Model Performance

During the completed walk-forward validation period, the final Linear Regression model achieved:

| Metric | Result |
|---|---:|
| MAE | **0.6255** |
| RMSE | **0.8706** |
| R² | **0.7395** |

### Interpretation

The MAE of approximately **0.63 percentage points** means that, on average, the model's forecast differed from the actual inflation value by around 0.63 percentage points during the evaluated walk-forward period.

The naive benchmark performed slightly better on RMSE and R² in the same evaluation.

Therefore, the project does **not** claim that the machine learning model universally outperforms the baseline.

The Linear Regression model was retained based on its MAE performance together with simplicity, interpretability, and suitability for the ongoing forecasting workflow.

---

# 🔮 Current Forecast

The latest available CPI observation in the project is **August 2026**.

The system generated the following next-month forecast:

```text
Data Through: August 2026
Forecast Month: September 2026
Predicted CPI Inflation: 4.87%
Model: Linear Regression
```

The September 2026 value is a **model forecast**, not an observed official CPI inflation value.

The forecast is generated using the latest available actual economic observations. Once September's official CPI data becomes available, the forecast can be evaluated against the actual value.

### Previous completed forecast

For August 2026:

```text
Forecast: 4.38%
Actual:   4.82%
Error:   -0.44 percentage points
```

The error convention used by the project is:

```text
error = predicted inflation - actual inflation
```

Therefore, a negative error indicates that the forecast was below the actual observed value.

---

# 🚨 Economic Shock Detection

In addition to forecasting inflation, the project contains an economic monitoring component.

The shock detection system looks for unusually large movements in:

- CPI inflation
- WPI inflation
- Brent crude oil
- USD/INR exchange rate

Rolling statistics are used to calculate z-scores.

A movement is flagged when:

```text
|z-score| ≥ 2
```

The system produces indicators such as:

```text
Inflation Shock
WPI Shock
Brent Oil Shock
USD/INR Shock
Overall Shock
```

### Important distinction

The shock detector is an **early-warning monitoring tool**.

It does not claim to predict unexpected economic shocks before they occur. Its purpose is to identify unusually large movements in selected economic indicators that may deserve further investigation.

---

# 🔄 Forecast History & Evaluation

Every generated forecast is stored in:

```text
data/processed/forecast_history.csv
```

The history records information such as:

- Forecast generation date
- Data available through
- Forecast month
- Predicted inflation
- Model used
- Shock indicators
- Actual inflation, when available
- Forecast error
- Absolute error
- Percentage error
- Evaluation status

The workflow is:

```text
Generate Forecast
       │
       ▼
Store Prediction
       │
       ▼
Wait for Official CPI
       │
       ▼
Actual Inflation Available
       │
       ▼
Calculate Forecast Error
       │
       ▼
Update Forecast History
```

This creates a persistent record that can be used to monitor forecasting performance over time.

---

# 🔁 Continuous Monthly Forecasting

The project is designed to support repeated monthly execution.

For each new month:

```text
New Official Data
       │
       ▼
Update Datasets
       │
       ▼
Validate Data
       │
       ▼
Build Features
       │
       ▼
Evaluate Previous Forecasts
       │
       ▼
Retrain Model
       │
       ▼
Generate Next-Month Forecast
       │
       ▼
Run Shock Detection
       │
       ▼
Store Forecast
```

The production pipeline is controlled by:

```text
run_pipeline.py
```

This means the project can continue producing new forecasts as additional monthly observations become available.

---

# 📊 Streamlit Dashboard

The project includes an interactive **Streamlit dashboard** for monitoring the forecasting system.

The dashboard provides:

- Current CPI inflation
- Next-month inflation forecast
- Data-through date
- Latest evaluated forecast error
- CPI inflation trend
- Forecast vs. actual values
- WPI inflation
- RBI repo rate
- Brent crude oil price
- USD/INR exchange rate
- Economic indicator trends
- Early warning shock signals
- Model information
- Training observation count and period

The dashboard is implemented in:

```text
app.py
```

Run it locally with:

```bash
streamlit run app.py
```

---

# 🗂️ Project Structure

```text
Inflation-Forecasting/
│
├── data/
│   ├── metadata/
│   │   └── data_sources.md
│   │
│   ├── raw/
│   │
│   └── processed/
│       ├── cpi_master.csv
│       ├── economic_master.csv
│       ├── economic_master_enriched.csv
│       ├── final_economic_master.csv
│       ├── food_beverages_master.csv
│       ├── forecast_history.csv
│       ├── repo_rate_master.csv
│       ├── wpi_master.csv
│       ├── crude_oil_master.csv
│       └── exchange_rate_master.csv
│
├── models/
│   └── final_inflation_model.pkl
│
├── notebooks/
│   ├── 01_cpi_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_final_inflation_model.ipynb
│
├── src/
│   ├── data_collection/
│   │   ├── download_cpi.py
│   │   ├── download_repo_rate.py
│   │   ├── download_wpi.py
│   │   ├── download_crude_oil.py
│   │   ├── download_exchange_rate.py
│   │   ├── build_economic_dataset.py
│   │   ├── build_enriched_economic_master.py
│   │   └── merge_food_beverages.py
│   │
│   ├── features/
│   │   └── build_features.py
│   │
│   ├── models/
│   │   └── train_model.py
│   │
│   ├── forecasting/
│   │   ├── run_forecast.py
│   │   └── evaluate_forecasts.py
│   │
│   └── monitoring/
│       └── shock_detection.py
│
├── app.py
├── run_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

Raw data and locally generated model files are excluded from version control according to `.gitignore`.

---

# 🛠️ Technologies Used

### Programming & Data

- Python
- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- XGBoost

### Statistical Forecasting

- Statsmodels
- ARIMA
- SARIMA

### Visualization & Exploration

- Matplotlib
- Jupyter Notebook

### Dashboard

- Streamlit

### Development

- Git
- GitHub
- VS Code

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Kashmira-s001/India-Inflation-Forecasting.git
```

Move into the project directory:

```bash
cd India-Inflation-Forecasting
```

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Run the Complete Pipeline

The recommended way to update the project and generate the latest forecast is:

```bash
python run_pipeline.py
```

The pipeline performs the following steps:

1. Updates CPI data
2. Updates RBI repo-rate data
3. Updates WPI data
4. Updates Brent crude oil data
5. Updates USD/INR exchange-rate data
6. Builds the economic master dataset
7. Builds the enriched economic master dataset
8. Merges Food & Beverages data
9. Evaluates previously generated forecasts
10. Retrains the final inflation model
11. Generates the next-month forecast

---

## Train the Model Separately

```bash
python src/models/train_model.py
```

This rebuilds the training dataset, trains the Linear Regression model, and saves it locally under:

```text
models/final_inflation_model.pkl
```

---

## Generate a Forecast Separately

```bash
python src/forecasting/run_forecast.py
```

This:

1. Loads the latest economic dataset
2. Builds forecasting features
3. Loads the trained model
4. Generates the next-month forecast
5. Runs economic shock detection
6. Stores the forecast in `forecast_history.csv`

---

## Evaluate Previous Forecasts

```bash
python src/forecasting/evaluate_forecasts.py
```

When official actual inflation becomes available, this script matches it with the corresponding stored forecast and calculates forecast errors.

---

## Launch the Dashboard

```bash
streamlit run app.py
```

---

# 📓 Notebooks

The notebooks document the development and analysis process.

### `01_cpi_exploration.ipynb`

Explores the CPI dataset and historical inflation behaviour.

### `02_feature_engineering.ipynb`

Develops time-series features and prepares the modelling dataset.

### `03_final_inflation_model.ipynb`

Documents the final model development and evaluation workflow.

The production scripts under `src/` are used for the reproducible forecasting pipeline.

---

# 📦 Data Handling

Raw datasets are not included in the public repository.

The repository contains processed datasets used for analysis and modelling.

Raw files are excluded through:

```text
data/raw/
```

and locally generated model files are excluded through:

```text
models/*.pkl
```

This keeps the repository lightweight while preserving the processed analytical data and reproducible code.

---

# ⚠️ Forecasting Limitations

This project is an experimental forecasting and analytical system. It should **not** be interpreted as an official inflation forecast from the Government of India or the Reserve Bank of India.

Important limitations include:

- Monthly observations provide a relatively small modelling sample.
- Inflation can be affected by sudden events that historical data cannot anticipate.
- Economic relationships can change over time.
- Model performance can vary across different economic regimes.
- Some economic indicators may be more useful for monitoring than for direct prediction.
- Forecast accuracy should be evaluated continuously as new observations become available.
- Data availability and publication timing can differ across economic indicators.

The project therefore treats forecasting as an **ongoing evaluation problem**, rather than assuming that one model will remain optimal forever.

---

# 🚀 Future Improvements

The core forecasting pipeline and dashboard are now implemented. Possible future improvements include:

### Model Development

- Test additional lag and seasonal features
- Explore richer macroeconomic feature sets
- Re-evaluate alternative models as more observations become available
- Compare model performance over different economic regimes

### Forecast Monitoring

- Expand the forecast history as more months are evaluated
- Add rolling performance metrics
- Monitor forecast bias and error stability
- Track model performance against the naive benchmark

### Deployment & Automation

- Deploy the Streamlit dashboard publicly
- Schedule the forecasting pipeline for monthly execution
- Add automated notifications when new forecasts are generated
- Improve handling of source-data release timing

### Economic Intelligence

- Add scenario analysis
- Study relationships between inflation and macroeconomic indicators
- Expand economic shock diagnostics
- Add explainability for model forecasts

---

# 📌 Project Status

## ✅ Core Project Completed

| Component | Status |
|---|---|
| CPI data pipeline | ✅ |
| WPI data pipeline | ✅ |
| RBI repo-rate pipeline | ✅ |
| Brent crude-oil pipeline | ✅ |
| USD/INR exchange-rate pipeline | ✅ |
| Food & Beverages data processing | ✅ |
| Economic master dataset | ✅ |
| Feature engineering | ✅ |
| Model comparison | ✅ |
| Walk-forward validation | ✅ |
| Final forecasting model | ✅ |
| Next-month forecasting | ✅ |
| Economic shock detection | ✅ |
| Forecast history | ✅ |
| Forecast evaluation | ✅ |
| Automated end-to-end pipeline | ✅ |
| Streamlit dashboard | ✅ |
| GitHub repository | ✅ |

The project is considered complete as a **working forecasting and economic-intelligence prototype**, while future improvements can continue independently.

---

# 👩‍💻 Author

## Kashmira Shelar

Integrated B.Sc.-M.Sc. in Data Science  
MGM University

GitHub:  
https://github.com/Kashmira-s001

---

## ⭐ Project Summary

**India Inflation Forecasting & Economic Intelligence System** combines economic data engineering, time-series feature engineering, machine learning, model validation, forecasting, shock detection, and interactive visualization into a single reproducible workflow.

The central idea is simple:

```text
Collect → Clean → Combine → Engineer → Validate
                    ↓
                 Forecast
                    ↓
          Monitor → Evaluate → Update
```

The system is designed to keep learning from newly available monthly economic observations rather than treating inflation forecasting as a one-time prediction task.
