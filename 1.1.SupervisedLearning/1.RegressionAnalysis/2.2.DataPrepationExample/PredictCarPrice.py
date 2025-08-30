import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("CarSaleData.csv")
print("Original Data:\n", data.head(), "\n")

# Features (X) and Target (y)
X = data.drop("Price", axis=1)
y = data["Price"]

# -----------------------------
# 1. Label Encoding (for ordinal-like or quick encoding)
# -----------------------------
label_encoder = LabelEncoder()
X_label_encoded = X.copy()
X_label_encoded["Brand"] = label_encoder.fit_transform(X["Brand"])
X_label_encoded["Color"] = label_encoder.fit_transform(X["Color"])
print("Label Encoded Data:\n", X_label_encoded.head(), "\n")

# -----------------------------
# 2. One-Hot Encoding (better for categorical data)
# -----------------------------
column_transformer = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(sparse_output=False, drop="first"), ["Brand", "Color"])
    ],
    remainder="passthrough"  # keep other columns
)

X_onehot = column_transformer.fit_transform(X)
X_onehot = pd.DataFrame(X_onehot, columns=column_transformer.get_feature_names_out())
print("One-Hot Encoded Data:\n", X_onehot.head(), "\n")

# -----------------------------
# 3. Normalization (Min-Max scaling: values between 0-1)
# -----------------------------
scaler_minmax = MinMaxScaler()
X_normalized = scaler_minmax.fit_transform(X_onehot)
print("Normalized Data (0-1 range):\n", pd.DataFrame(X_normalized).head(), "\n")

# -----------------------------
# 4. Standardization (mean=0, std=1)
# -----------------------------
scaler_standard = StandardScaler()
X_standardized = scaler_standard.fit_transform(X_onehot)
print("Standardized Data (mean=0, std=1):\n", pd.DataFrame(X_standardized).head(), "\n")

# -----------------------------
# 5. Linear Regression Model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X_standardized, y, test_size=0.3, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print("Model Coefficients:", model.coef_)
print("Model Intercept:", model.intercept_)
print("Train R^2 Score:", model.score(X_train, y_train))
print("Test R^2 Score:", model.score(X_test, y_test))
