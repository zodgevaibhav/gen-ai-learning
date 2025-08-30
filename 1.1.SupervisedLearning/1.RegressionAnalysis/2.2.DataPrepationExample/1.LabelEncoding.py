import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("CarSaleData.csv")
# print("Original Data:\n", data.head(), "\n")

# Features (X) and Target (y)
X = data.drop("Price", axis=1)
y = data["Price"]

# -----------------------------
# 1. Label Encoding (for ordinal-like or quick encoding)
# -----------------------------
label_encoder_brand = LabelEncoder()
label_encoder_color = LabelEncoder()
X_label_encoded = X.copy()
X_label_encoded["Brand"] = label_encoder_brand.fit_transform(X["Brand"])
X_label_encoded["Color"] = label_encoder_color.fit_transform(X["Color"])

for i, item in enumerate(label_encoder_brand.classes_):
    print(f"Label {i} is for {item}")

print("--------------------------------------- \n")
for i, item in enumerate(label_encoder_color.classes_):
    print(f"Label {i} is for {item}")

print("\nLabel Encoded Data:\n", X_label_encoded.head(), "\n")