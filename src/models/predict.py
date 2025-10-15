# src/models/predict.py
import os
import pandas as pd
import joblib
import numpy as np

# Paths (adjust if you moved files)
MODEL_PATH = "models/xgb_model.pkl"
TRAIN_FEATURES_PATH = "data/processed/features.csv"  # used to recover District categories/order
INPUT_FEATURES_PATH = "data/processed/features.csv"  # default input; can be changed to another CSV
OUTPUT_PATH = "data/processed/predictions.csv"


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Train the model first.")
    model = joblib.load(path)
    return model


def load_training_categories(path=TRAIN_FEATURES_PATH):
    """
    Load the training features file to recover categorical mapping information
    (e.g., District categories in the order used at training).
    """
    if not os.path.exists(path):
        return None
    df_train = pd.read_csv(path)
    if "District" in df_train.columns:
        # preserve the category order used in training (order of appearance)
        cats = pd.Categorical(df_train["District"].astype(str)).categories.tolist()
        return cats
    return None


def encode_district_with_training_cats(df, training_cats):
    """
    Encode District column to integer codes using training categories order.
    New/unseen districts are assigned the next new code (len(training_cats)).
    """
    s = df["District"].astype(str)
    if training_cats is None:
        # fallback: use categories observed in this df
        codes = pd.Categorical(s).codes
        # ensure non-negative
        codes = np.where(codes < 0, len(np.unique(codes)), codes)
        return codes

    cat = pd.Categorical(s, categories=training_cats)
    codes = cat.codes  # -1 for unseen
    # replace unseen (-1) with a new code = len(training_cats)
    unseen_mask = codes == -1
    if unseen_mask.any():
        new_code = len(training_cats)
        codes = codes.astype(int)
        codes[unseen_mask] = new_code
    return codes


def prepare_dataframe_for_model(df, model, training_cats=None):
    """
    Prepare the dataframe so its columns and dtypes match the model's expectations.
    - Drop future target column if present
    - Encode District using training categories
    - Convert Date -> ordinal integer
    - Reorder columns to model.get_booster().feature_names
    """
    # Work on a copy
    df_proc = df.copy()

    # Drop future target if present
    if "future_7d_sum" in df_proc.columns:
        df_proc = df_proc.drop(columns=["future_7d_sum"])

    # Encode District if present
    if "District" in df_proc.columns:
        df_proc["District"] = encode_district_with_training_cats(df_proc, training_cats)

    # Convert Date to ordinal (int) if present
    if "Date" in df_proc.columns:
        df_proc["Date"] = pd.to_datetime(df_proc["Date"], errors="coerce")
        df_proc["Date"] = df_proc["Date"].map(lambda x: x.toordinal() if pd.notna(x) else -1).astype(int)

    # Ensure numeric dtypes for remaining object-like columns (if any)
    # If you have other categorical columns, you should encode them similarly.
    for col in df_proc.columns:
        if df_proc[col].dtype == "object":
            # try to coerce to numeric; if fails, convert to categorical codes
            coerced = pd.to_numeric(df_proc[col], errors="coerce")
            if coerced.notna().sum() > 0:
                df_proc[col] = coerced.fillna(0)
            else:
                df_proc[col] = pd.Categorical(df_proc[col].astype(str)).codes

    # Reorder/filter columns to match model feature names
    # model.get_booster().feature_names returns list in training order
    booster = model.get_booster()
    expected = booster.feature_names  # list
    if expected is None:
        raise ValueError("Could not retrieve feature names from model. Ensure model was trained with feature names.")

    # Check expected features exist in df_proc
    missing = [c for c in expected if c not in df_proc.columns]
    if missing:
        raise ValueError(f"Input data is missing the following expected feature columns required by the model: {missing}")

    # Filter and reorder
    X = df_proc[expected].copy()

    # Ensure numeric dtype
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    return X


def make_predictions(input_csv_path=None, output_path=OUTPUT_PATH):
    """
    Main entrypoint:
    - If input_csv_path is None -> uses INPUT_FEATURES_PATH (features.csv)
    - Loads model, loads training categories, prepares data, predicts, saves output
    """
    model = load_model()
    training_cats = load_training_categories(TRAIN_FEATURES_PATH)

    # Load input
    input_path = input_csv_path if input_csv_path else INPUT_FEATURES_PATH
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at {input_path}")

    df_in = pd.read_csv(input_path)

    # Keep a copy for output
    df_out = df_in.copy()

    # Prepare X
    X = prepare_dataframe_for_model(df_in, model, training_cats=training_cats)

    # Predict
    preds = model.predict(X)
    df_out["Prediction"] = preds
    # Map to readable labels
    df_out["Prediction_Label"] = df_out["Prediction"].map({0: "No outbreak", 1: "Outbreak"})

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_out.to_csv(output_path, index=False)
    print(f"✅ Predictions saved to: {output_path}")

    # Print readable preview
    preview_cols = [c for c in ["Date", "District", "Cases", "Prediction_Label"] if c in df_out.columns]
    print("\nSample Predictions:")
    print(df_out[preview_cols].head(10).to_string(index=False))

    return df_out


if __name__ == "__main__":
    make_predictions()
