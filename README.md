# 🇮🇳 India Inflation Forecasting & Economic Intelligence System

A data-driven forecasting system for predicting **India's next-month CPI inflation** using historical inflation patterns and selected macroeconomic indicators.

The project is designed as an **ongoing monthly forecasting pipeline** rather than a one-time machine learning experiment. As new economic data becomes available, the system can update the dataset, generate a new forecast, store the prediction, and later evaluate it against the actual inflation value.

---

## 📌 Overview

Inflation is one of the most important indicators of economic conditions. It is influenced by domestic price movements as well as factors such as wholesale prices, monetary policy, crude oil prices, and exchange rates.

This project explores whether these economic signals can be used to forecast India's **Consumer Price Index (CPI) inflation one month ahead**.

The system combines:

- Historical CPI inflation
- WPI inflation
- RBI repo rate
- Brent crude oil prices
- USD/INR exchange rate
- Food & Beverages CPI data
- Time-series feature engineering
- Machine learning and statistical forecasting
- Economic shock detection
- Forecast history and evaluation

The goal is not simply to build the most complicated model, but to develop a **transparent, reproducible, and continuously updateable forecasting workflow**.

---

# 🎯 Objective

The primary forecasting objective is:

> **Using information available up to month `t`, forecast India's CPI inflation for month `t + 1`.**

For example:

```text
July 2026 Economic Data
          │
          ▼
   Feature Engineering
          │
          ▼
    Forecasting Model
          │
          ▼
August 2026 CPI Inflation
````

As new monthly observations become available, the same process can be repeated for subsequent months.

---

# 📊 Data

The project works with monthly economic data covering approximately **2013 onwards**, with the final modelling dataset extending through the latest available month.

The main indicators include:

| Indicator             | Role in the Project                            |
| --------------------- | ---------------------------------------------- |
| CPI Inflation         | Primary forecasting target                     |
| WPI Inflation         | Indicator of wholesale price pressure          |
| Repo Rate             | Monetary policy indicator                      |
| Brent Crude Oil       | Energy and global commodity price indicator    |
| USD/INR Exchange Rate | Currency and imported-price pressure indicator |
| Food & Beverages CPI  | Food-related price analysis                    |

The project stores cleaned and processed datasets under:

```text
data/processed/
```

Raw source files are intentionally excluded from the GitHub repository.

Detailed information about the datasets and their sources is available in:

```text
data/metadata/data_sources.md
```

---

# 🏛️ Data Sources

The project uses official and publicly available economic data sources.

Major sources include:

* Ministry of Statistics and Programme Implementation (MoSPI)
* e-Sankhyiki
* Reserve Bank of India (RBI)
* Office of Economic Adviser / WPI data
* World Bank Commodity Markets
* Publicly available exchange-rate data

The exact source, coverage, transformation, and usage of each dataset are documented in:

```text
data/metadata/data_sources.md
```

---

# 🧹 Data Processing Pipeline

The project follows a structured data-processing workflow.

```text
Raw Economic Data
       │
       ▼
Data Inspection
       │
       ▼
Cleaning & Validation
       │
       ▼
Monthly Alignment
       │
       ▼
Individual Master Datasets
       │
       ▼
Economic Master Dataset
       │
       ▼
Feature Engineering
       │
       ▼
Forecasting Dataset
```

Each major economic indicator is processed separately before being combined into the final modelling dataset.

---

# 🧠 Feature Engineering

The forecasting problem is formulated as a one-step-ahead time-series prediction problem.

The target variable is created as:

```text
target_next_month_inflation
```

which represents the CPI inflation value in the following month.

The final forecasting model uses four features:

```text
inflation
inflation_lag_1
inflation_lag_12
wpi_inflation
```

### Feature descriptions

| Feature            | Description                                        |
| ------------------ | -------------------------------------------------- |
| `inflation`        | Current CPI inflation                              |
| `inflation_lag_1`  | CPI inflation from the previous month              |
| `inflation_lag_12` | CPI inflation from the same month one year earlier |
| `wpi_inflation`    | Current WPI inflation                              |

The lag features allow the model to capture both **recent inflation momentum** and **year-over-year seasonal/historical patterns**.

---

# 🤖 Models Evaluated

Multiple forecasting approaches were evaluated during model development.

### Machine Learning Models

* Linear Regression
* Ridge Regression
* Random Forest
* XGBoost

### Statistical Time-Series Models

* ARIMA
* SARIMA

### Baseline

* Naive persistence forecast

The naive baseline is important because inflation is a persistent time series. A machine learning model should therefore demonstrate value beyond simply assuming that the next month's inflation will remain close to the current value.

---

# 📈 Model Selection

The final model is:

## Linear Regression

using:

```text
inflation
inflation_lag_1
inflation_lag_12
wpi_inflation
```

The final model was selected based primarily on **Mean Absolute Error (MAE)** during walk-forward validation, while the naive model is retained as a benchmark.

The final model is intentionally simple because the dataset contains a relatively small number of monthly observations. More complex models such as Random Forest and XGBoost did not consistently improve forecasting performance.

---

# 🧪 Model Validation

Because this is a time-series problem, random train-test splitting was avoided.

Instead, the project uses:

### 1. Chronological Validation

Historical observations are divided chronologically into training and testing periods.

```text
Past Data ───────────────► Future Data
   Train                       Test
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

This better represents how the model would operate in a real forecasting environment.

---

# 📊 Final Model Performance

The final Linear Regression model achieved the following performance during walk-forward validation:

| Metric |     Result |
| ------ | ---------: |
| MAE    | **0.6255** |
| RMSE   | **0.8706** |
| R²     | **0.7395** |

### Interpretation

The MAE of approximately **0.63 percentage points** means that, on average, the model's forecast differed from the actual inflation value by around 0.63 percentage points during the evaluated walk-forward period.

The naive benchmark remains important because it performed slightly better on RMSE and R² in the same evaluation.

Therefore, the project does **not** claim that the machine learning model universally outperforms the baseline.

Instead, the final model was selected based on its MAE performance, simplicity, interpretability, and suitability for the project's ongoing forecasting workflow.

---

# 🔮 Current Forecast

Using economic information available through **July 2026**, the system generated:

```text
Forecast Month: August 2026
Predicted CPI Inflation: 4.38%
Model: Linear Regression
```

This value is a **model forecast**, not the actual August 2026 inflation observation.

The actual value can be incorporated into the forecast history once the official August CPI data becomes available.

---

# 🚨 Economic Shock Detection

In addition to forecasting inflation, the project contains an economic monitoring component.

The shock detection system looks for unusually large movements in:

* CPI inflation
* WPI inflation
* Brent crude oil
* USD/INR exchange rate

Rolling statistics are used to calculate z-scores.

A movement is flagged when:

```text
|z-score| ≥ 2
```

The system produces indicators such as:

```text
Inflation Shock
WPI Shock
Brent Shock
USD/INR Shock
Overall Shock
```

### Important distinction

The shock detector is an **early-warning monitoring tool**.

It does not claim to predict unexpected economic shocks before they occur.

Its purpose is to identify unusually large movements in economic indicators that may deserve further investigation.

---

# 🔄 Forecast History

Every generated forecast can be stored in:

```text
data/processed/forecast_history.csv
```

The history records information such as:

* Forecast generation date
* Data available through
* Forecast month
* Predicted inflation
* Model used
* Shock indicators

Once the actual inflation value becomes available, the prediction can be compared with the observed value.

```text
Forecast
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
Update Performance History
```

This creates the foundation for long-term monitoring of model performance.

---

# 🔁 Continuous Monthly Forecasting

The long-term objective is to operate the project as an ongoing forecasting system.

For each new month:

```text
New Official Data
       │
       ▼
Update Dataset
       │
       ▼
Validate Data
       │
       ▼
Build Features
       │
       ▼
Generate Forecast
       │
       ▼
Run Shock Detection
       │
       ▼
Store Forecast
       │
       ▼
Wait for Actual CPI
       │
       ▼
Evaluate Forecast
```

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

The project is therefore being developed as a **living forecasting pipeline** rather than a static model.

---

# 🗂️ Project Structure

```text
Inflation-Forecasting/
│
├── data/
│   ├── metadata/
│   │   └── data_sources.md
│   │
│   └── processed/
│       ├── cpi_master.csv
│       ├── cpi_wpi_master.csv
│       ├── crude_oil_master.csv
│       ├── economic_master.csv
│       ├── economic_master_enriched.csv
│       ├── exchange_rate_master.csv
│       ├── final_economic_master.csv
│       ├── food_beverages_2026.csv
│       ├── food_beverages_master.csv
│       ├── forecast_history.csv
│       ├── modeling_dataset.csv
│       ├── repo_rate_master.csv
│       └── wpi_master.csv
│
├── notebooks/
│   ├── 01_cpi_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_final_inflation_model.ipynb
│
├── src/
│   ├── data_collection/
│   │   ├── build_cpi_dataset.py
│   │   ├── build_crude_oil_dataset.py
│   │   ├── build_economic_dataset.py
│   │   ├── build_enriched_economic_master.py
│   │   ├── build_exchange_rate_dataset.py
│   │   ├── build_food_beverages_2026.py
│   │   ├── build_food_beverages_dataset.py
│   │   ├── build_repo_dataset.py
│   │   ├── build_wpi_dataset.py
│   │   └── validation scripts
│   │
│   ├── features/
│   │   └── build_features.py
│   │
│   ├── models/
│   │   └── train_model.py
│   │
│   ├── forecasting/
│   │   ├── predict_next_month.py
│   │   ├── run_forecast.py
│   │   └── evaluate_forecasts.py
│   │
│   └── monitoring/
│       └── shock_detection.py
│
├── models/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Technologies Used

### Programming & Data

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* XGBoost

### Statistical Forecasting

* Statsmodels
* ARIMA
* SARIMA

### Visualization & Exploration

* Matplotlib
* Jupyter Notebook

### Application

* Streamlit

### Development

* Git
* GitHub
* VS Code

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

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Train the Final Model

```bash
python -m src.models.train_model
```

This trains the final Linear Regression model and saves the model locally.

---

## Generate a Next-Month Forecast

```bash
python -m src.forecasting.predict_next_month
```

The script identifies the latest valid economic observation and generates a forecast for the following month.

---

## Run the Complete Forecasting Pipeline

```bash
python -m src.forecasting.run_forecast
```

This pipeline:

1. Loads the latest economic dataset
2. Builds forecasting features
3. Generates the next-month prediction
4. Runs economic shock detection
5. Stores the forecast in forecast history

---

## Evaluate Previous Forecasts

```bash
python -m src.forecasting.evaluate_forecasts
```

Once actual inflation values become available, this script can compare previous predictions with the observed values and calculate forecast errors.

---

# 📓 Notebooks

The notebooks document the development process.

### `01_cpi_exploration.ipynb`

Explores the CPI dataset and historical inflation behaviour.

### `02_feature_engineering.ipynb`

Develops time-series features and prepares the modelling dataset.

### `03_final_inflation_model.ipynb`

Contains the final model development and evaluation workflow.

The production scripts under `src/` are used for the reproducible forecasting pipeline.

---

# 📁 Data Handling

Raw datasets are not included in the public repository.

The repository contains processed datasets required for analysis and modelling.

Raw files are excluded through `.gitignore`:

```text
data/raw/
```

This keeps the repository lightweight while preserving the processed analytical data and code used to build the forecasting system.

---

# ⚠️ Forecasting Limitations

This project is an experimental forecasting and analytical system and should not be interpreted as an official inflation forecast.

Important limitations include:

* Monthly observations provide a relatively small modelling sample.
* Inflation can be affected by sudden events that historical data cannot anticipate.
* Economic relationships can change over time.
* Model performance can vary across different economic regimes.
* Some economic indicators may be more useful for monitoring than for direct prediction.
* Forecast accuracy should be evaluated continuously as new observations become available.

The project therefore treats forecasting as an **ongoing evaluation problem**, rather than assuming that one model will remain optimal forever.

---

# 🚧 Future Improvements

The project is currently under development.

Planned improvements include:

### Automated Data Updates

Automatically retrieve newly released official economic data.

### Automated Forecasting

Run the forecasting pipeline whenever new monthly data becomes available.

### Forecast Dashboard

Develop an interactive Streamlit dashboard displaying:

* Latest CPI inflation
* Forecast inflation
* Historical inflation
* WPI inflation
* Repo rate
* Brent crude oil
* USD/INR
* Forecast errors
* Economic shock indicators

### Forecast Performance Tracking

Track:

* MAE
* RMSE
* Forecast bias
* Rolling forecast performance
* Model vs. naive benchmark

### Model Monitoring

Monitor whether model performance deteriorates over time and evaluate whether retraining or model changes are necessary.

### Economic Scenario Analysis

Explore how changes in major economic indicators could influence the inflation outlook.

---

# 📌 Project Status

**🚧 In Development**

Current components:

* [x] CPI data pipeline
* [x] WPI data pipeline
* [x] Repo rate data pipeline
* [x] Brent crude oil data pipeline
* [x] USD/INR exchange-rate pipeline
* [x] Food & Beverages data processing
* [x] Feature engineering
* [x] Model comparison
* [x] Walk-forward validation
* [x] Final forecasting model
* [x] Next-month forecasting script
* [x] Economic shock detection
* [x] Forecast history
* [x] Forecast evaluation framework
* [x] GitHub repository
* [ ] Automated monthly data updates
* [ ] Automated model retraining
* [ ] Streamlit forecasting dashboard
* [ ] Long-term forecast performance monitoring

---

# 👩‍💻 Author

## Kashmira Shelar

Integrated B.Sc.-M.Sc. in Data Science
MGM University

GitHub:
[https://github.com/Kashmira-s001](https://github.com/Kashmira-s001)

---

# ⭐ Why This Project?

This project was built to explore the intersection of:

**Data Science + Time-Series Forecasting + Economics**

Rather than treating inflation forecasting as only a machine-learning problem, the project focuses on building an end-to-end analytical system that combines:

```text
Official Economic Data
        +
Data Engineering
        +
Time-Series Analysis
        +
Machine Learning
        +
Economic Monitoring
        +
Continuous Evaluation
```

The ultimate goal is to develop a forecasting workflow that becomes more useful over time as new economic observations and forecast results accumulate.
