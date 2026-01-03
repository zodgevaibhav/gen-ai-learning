"""
Fraud Detection Model Training using XGBoost (Refactored)
--------------------------------------------------------

Supports:
- ML training data
- Rule-compatible fraud datasets
- Large feature sets
- Boolean & numeric features

Input  : CSV training file
Output : fraud_xgboost_model.joblib
"""

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from joblib import dump
import sys

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

DATA_FILE = "/Users/vzodge/Documents/ALL_GITHUB_REPO/gen-ai-learning/6.AgenticAI/6.CardPaymentFraudDetection/1.CodeGenerator/taining_data/rule_compatible_fraud_data.csv"
MODEL_FILE = "fraud_xgboost_model.joblib"

TARGET_COL = "label"
ID_COLS = ["transaction_id"]

TEST_SIZE = 0.2
RANDOM_STATE = 42
THRESHOLD = 0.5

# Optional: explicitly exclude rule-only features if needed
EXCLUDE_FEATURES = [
    "label",
    "transaction_id"
]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        print(f"✅ Loaded data: {df.shape}")
        return df
    except Exception as e:
        print("❌ Failed to load data:", e)
        sys.exit(1)

df = load_data(DATA_FILE)

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

if TARGET_COL not in df.columns:
    raise ValueError("❌ label column not found")

# --------------------------------------------------
# FEATURE PREPROCESSING
# --------------------------------------------------

def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Drop ID columns
    - Convert booleans to int
    - Fill missing values safely
    """
    df = df.copy()

    # Drop ID columns
    for col in ID_COLS:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Convert booleans → int
    bool_cols = df.select_dtypes(include=["bool"]).columns
    for col in bool_cols:
        df[col] = df[col].astype(int)

    # Fill missing numeric values
    df.fillna(0, inplace=True)

    return df

X = preprocess_features(df.drop(columns=[TARGET_COL]))
y = df[TARGET_COL]

print(f"📊 Total features used: {X.shape[1]}")

# --------------------------------------------------
# CLASS IMBALANCE HANDLING
# --------------------------------------------------

fraud_count = int(y.sum())
genuine_count = len(y) - fraud_count

if fraud_count == 0:
    raise ValueError("❌ No fraud samples found")

scale_pos_weight = genuine_count / fraud_count

print(f"⚖️ Fraud: {fraud_count}, Genuine: {genuine_count}")
print(f"⚖️ scale_pos_weight = {scale_pos_weight:.2f}")

# --------------------------------------------------
# TRAIN / VALIDATION SPLIT
# --------------------------------------------------

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE
)

print(f"🧪 Train size: {X_train.shape}")
print(f"🧪 Validation size: {X_val.shape}")

# --------------------------------------------------
# MODEL DEFINITION
# --------------------------------------------------

model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="auc",
    n_estimators=400,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    tree_method="hist",
    random_state=RANDOM_STATE
)

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

print("🚀 Training XGBoost fraud model...")

model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    verbose=True
)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

y_val_proba = model.predict_proba(X_val)[:, 1]
y_val_pred = (y_val_proba >= THRESHOLD).astype(int)

print("\n📈 ROC AUC:", roc_auc_score(y_val, y_val_proba))
print("\n📄 Classification Report:")
print(classification_report(y_val, y_val_pred))
print("\n🧮 Confusion Matrix:")
print(confusion_matrix(y_val, y_val_pred))

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

dump(model, MODEL_FILE)
print(f"\n💾 Model saved to {MODEL_FILE}")

# --------------------------------------------------
# FEATURE IMPORTANCE (Optional but useful)
# --------------------------------------------------

importance = (
    pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    })
    .sort_values(by="importance", ascending=False)
)

print("\n🔍 Top 15 Features:")
print(importance.head(15))
