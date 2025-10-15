import pandas as pd
import os

# --- Config paths ---
RAW_DATA_PATH = "data/raw/telangana_health_dataset2025.csv"
PROCESSED_DATA_PATH = "data/processed/cleaned_data.csv"

# --- Season mapping function ---
def month_to_season(month: int) -> str:
    if month in [3, 4, 5]:
        return "summer"
    elif month in [6, 7, 8, 9]:
        return "rainy"
    elif month in [10, 11]:
        return "monsoon"
    else:
        return "winter"

def clean_dataset():
    # Load dataset
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw dataset not found at {RAW_DATA_PATH}")
    
    df = pd.read_csv(RAW_DATA_PATH)

    # Ensure Date column is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Add season column
    df["month"] = df["Date"].dt.month
    df["season"] = df["month"].apply(month_to_season)

    # Drop helper column
    df = df.drop(columns=["month"])

    # Save cleaned dataset
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"✅ Cleaned dataset saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    clean_dataset()
