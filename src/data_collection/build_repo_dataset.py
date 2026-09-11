import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

RBI_FILE = RAW_DATA / "rbi_key_rates.xlsx"
OUTPUT_FILE = PROCESSED_DATA / "repo_rate_master.csv"


# ============================================================
# 2. LOAD RAW RBI WORKBOOK
# ============================================================

print("Loading RBI key-rate data...")

raw = pd.read_excel(
    RBI_FILE,
    sheet_name="Report 1",
    header=None
)


# ============================================================
# 3. EXTRACT EFFECTIVE DATE + REPO
# ============================================================
# RBI workbook layout:
# column 1 -> Effective Date
# column 3 -> Repo Rate
#
# Actual observations begin from row 8.

repo = raw.iloc[8:, [1, 3]].copy()

repo.columns = [
    "effective_date",
    "repo_rate"
]


# ============================================================
# 4. CLEAN VALUES
# ============================================================

repo["effective_date"] = pd.to_datetime(
    repo["effective_date"],
    errors="coerce"
)

repo["repo_rate"] = pd.to_numeric(
    repo["repo_rate"],
    errors="coerce"
)


# Keep only rows where repo rate is explicitly reported

repo = repo.dropna(
    subset=["effective_date", "repo_rate"]
)


# ============================================================
# 5. SORT POLICY CHANGES
# ============================================================

repo = repo.sort_values(
    "effective_date"
).reset_index(drop=True)


print("\nRepo-rate change observations:")
print(repo.tail(15).to_string(index=False))


# ============================================================
# 6. CREATE MONTHLY TIMELINE
# ============================================================

start_date = pd.Timestamp("2013-01-01")

# Historical RBI export currently ends in Dec 2025
end_date = pd.Timestamp("2026-07-01")

monthly = pd.DataFrame({
    "date": pd.date_range(
        start=start_date,
        end=end_date,
        freq="MS"
    )
})


# ============================================================
# 7. FIND RATE APPLICABLE AT EACH MONTH-END
# ============================================================

monthly["month_end"] = (
    monthly["date"]
    + pd.offsets.MonthEnd(0)
)

monthly = pd.merge_asof(
    monthly.sort_values("month_end"),
    repo.sort_values("effective_date"),
    left_on="month_end",
    right_on="effective_date",
    direction="backward"
)


# ============================================================
# 8. EXTEND THROUGH JULY 2026
# ============================================================
# RBI's official current-rate information shows the
# Policy Repo Rate at 5.25% during July 2026.

monthly.loc[
    monthly["date"] >= pd.Timestamp("2026-01-01"),
    "repo_rate"
] = 5.25


# ============================================================
# 9. KEEP FINAL COLUMNS
# ============================================================

repo_master = monthly[
    [
        "date",
        "repo_rate"
    ]
].copy()


# ============================================================
# 10. SAVE
# ============================================================

repo_master.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved to: {OUTPUT_FILE}")