import os
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Paths
FEATURES_PATH = os.path.join("data", "processed", "features.csv")
MODEL_PATH = os.path.join("models", "xgb_model.pkl")

def train():
    print(f"Loading features from: {os.path.abspath(FEATURES_PATH)}")
    df = pd.read_csv(FEATURES_PATH)

    # Target variable
    y = (df["future_7d_sum"] > 0).astype(int)

    # Drop target column from features
    X = df.drop(columns=["future_7d_sum"])

    # ---- FIX: Encode non-numeric columns ----
    if "District" in X.columns:
        X["District"] = X["District"].astype("category").cat.codes
    if "Date" in X.columns:
        X["Date"] = pd.to_datetime(X["Date"], errors="coerce")
        X["Date"] = X["Date"].map(pd.Timestamp.toordinal)  # convert to number

    print(f"Dataset shape: {X.shape} Positive ratio: {y.mean():.2f}")

    # Split
    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )

    # Early stopping with constructor param instead of fit
    model.set_params(early_stopping_rounds=10)

    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        verbose=False
    )

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to: {MODEL_PATH}")

    # Evaluation
    y_pred = model.predict(X_val)
    print("\nClassification Report:\n", classification_report(y_val, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_val, y_pred))


if __name__ == "__main__":
    train()
