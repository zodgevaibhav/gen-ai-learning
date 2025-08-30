import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("CarSaleData.csv")

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