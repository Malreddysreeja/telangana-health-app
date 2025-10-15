# src/data/features.py
from pathlib import Path
import pandas as pd
import numpy as np
import os

ROOT = Path(__file__).resolve().parents[2]
CLEANED = ROOT / "data" / "processed" / "cleaned_data.csv"
OUT = ROOT / "data" / "processed" / "features.csv"

def make_features():
    if not CLEANED.exists():
        raise FileNotFoundError(f"Cleaned data not found at {CLEANED}. Run data_cleaning.py first.")

    print("Loading cleaned data from:", CLEANED)
    df = pd.read_csv(CLEANED, parse_dates=["Date"], infer_datetime_format=True)

    # Ensure necessary columns exist
    if "District" not in df.columns or "Cases" not in df.columns:
        raise KeyError("Input must contain 'District' and 'Cases' columns")

    # Aggregate to district-date level
    daily = (
        df.groupby(["District", "Date"], as_index=False)
        .agg({"Cases": "sum", "Mortality": "sum"})
        .sort_values(["District", "Date"])
    )

    # Feature generation per district
    lags = [1,2,3,7,14]
    rolls = [7,14]

    all_parts = []
    for district, g in daily.groupby("District"):
        g = g.sort_values("Date").reset_index(drop=True)
        # create lag features
        for lag in lags:
            g[f"cases_lag_{lag}"] = g["Cases"].shift(lag)
        # rolling means
        for w in rolls:
            g[f"cases_roll_{w}"] = g["Cases"].rolling(window=w, min_periods=1).mean()
        # incidence per 100k if Population exists; otherwise keep absolute 7-day sum
        if "Population" in g.columns:
            pop = g["Population"].iloc[0] if not pd.isna(g["Population"].iloc[0]) else 100000
            g["incidence_7d_per_100k"] = g["Cases"].rolling(7, min_periods=1).sum() / (pop / 100000)
        else:
            g["incidence_7d_per_100k"] = g["Cases"].rolling(7, min_periods=1).sum()
        # future 7-day sum (label candidate) - shifted so current row has future sum
        g["future_7d_sum"] = g["Cases"].rolling(window=7, min_periods=1).sum().shift(-6)
        all_parts.append(g)

    features = pd.concat(all_parts, ignore_index=True)

    # Drop rows where all lag features are NaN (early days)
    lag_cols = [c for c in features.columns if c.startswith("cases_lag_")]
    features = features.dropna(subset=lag_cols, how="all").reset_index(drop=True)

    # Save
    os.makedirs(OUT.parent, exist_ok=True)
    features.to_csv(OUT, index=False)
    print("Saved features to:", OUT)
    print("Rows:", len(features))
    print("Columns:", list(features.columns))

if __name__ == "__main__":
    make_features()
