# Data Scaling Example
# Scaling means transforming data to a specific range
# Two common techniques are Normalization and Standardization   
# MinMaxScaler (Normalization) : Scales data to a fixed range - usually 0 to 1
# StandardScaler (Standardization) : Scales data to have mean=0 and variance=1
## Which means it centers the data around 0 and scales it based on standard deviation
## Example : If mean=50 and std=10, then value 60 will be transformed to (60-50)/10 = 1

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# -----------------------------
# 1. Create sample dataset
# -----------------------------
df = pd.read_csv("SpendingData.csv")
X=df.drop('Spendings', axis=1)  # Features: all columns except 'Spending Score (1-100)'
y=df['Spendings']  # Target: 'Spending

lr = LinearRegression()
lr.fit(X, y)
print("Without Scaling:")
print("Coefficients:", lr.coef_)
print("Intercept:", lr.intercept_)
print("Predictions:", lr.predict(pd.DataFrame([[50,45611]],columns=['Age','Salary'])), "\n")

# -----------------------------
# 3. Normalization (Min-Max scaling: values between 0-1)
# -----------------------------
scaler_minmax = MinMaxScaler()
X_normalized = scaler_minmax.fit_transform(X)

print("Original Data:\n", pd.DataFrame(X).head(), "\n")
print("Normalized Data (0-1 range):\n", pd.DataFrame(X_normalized).head(), "\n")


# -----------------------------
# 3. Linear Regression with StandardScaler
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lr_scaled = LinearRegression()
lr_scaled.fit(X_scaled, y)

print("With Scaling:")
print("Coefficients:", lr_scaled.coef_)
print("Intercept:", lr_scaled.intercept_)
print("Predictions:", lr_scaled.predict(pd.DataFrame([[50,45611]])), "\n")
