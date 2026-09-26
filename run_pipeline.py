import subprocess
import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent


# ============================================================
# PIPELINE STEPS
# ============================================================

PIPELINE_STEPS = [
    ("Updating CPI", "src/data_collection/download_cpi.py"),
    ("Updating RBI repo rate", "src/data_collection/download_repo_rate.py"),
    ("Updating WPI", "src/data_collection/download_wpi.py"),
    ("Updating Brent crude oil", "src/data_collection/download_crude_oil.py"),
    ("Updating USD/INR exchange rate", "src/data_collection/download_exchange_rate.py"),
    ("Building economic master", "src/data_collection/build_economic_dataset.py"),
    ("Building enriched economic master", "src/data_collection/build_enriched_economic_master.py"),
    ("Merging Food & Beverages data", "src/data_collection/merge_food_beverages.py"),
    ("Evaluating previous forecasts", "src/forecasting/evaluate_forecasts.py"),
    ("Retraining inflation model", "src/models/train_model.py"),
    ("Generating next-month forecast", "src/forecasting/run_forecast.py"),
]


# ============================================================
# RUN ONE STEP
# ============================================================

def run_step(name, script):

    print("\n")
    print("=" * 70)
    print(name)
    print("=" * 70)

    script_path = PROJECT_ROOT / script

    result = subprocess.run(
        [
            sys.executable,
            str(script_path)
        ],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:

        print("\n" + "=" * 70)
        print(f"PIPELINE STOPPED: {name}")
        print("=" * 70)

        sys.exit(
            result.returncode
        )


# ============================================================
# MAIN PIPELINE
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("INDIA INFLATION FORECASTING PIPELINE")
    print("=" * 70)

    print(
        "\nProject:",
        PROJECT_ROOT
    )

    for name, script in PIPELINE_STEPS:

        run_step(
            name,
            script
        )

    print("\n")
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        "\nLatest economic data and forecast have been updated."
    )