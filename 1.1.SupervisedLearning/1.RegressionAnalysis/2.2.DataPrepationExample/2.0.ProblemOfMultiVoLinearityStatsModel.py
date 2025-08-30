import pandas as pd
import statsmodels.api as sm
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Load dataset
if not os.path.exists("SalaryData.csv"):
	sys.exit("Error: 'SalaryData.csv' not found in the current directory.")

data = pd.read_csv("SalaryData.csv")
required_columns = {"Title", "Experience", "Salary"}
if not required_columns.issubset(data.columns):
	sys.exit(f"Error: CSV file must contain columns: {required_columns}")

y = data["Salary"]

# --- Case 1: Keeping ALL dummy variables (multicollinearity problem) ---
dummies_all = pd.get_dummies(data["Title"], drop_first=False)
X_all = pd.concat([data[["Experience"]], dummies_all], axis=1)
X_all = sm.add_constant(X_all)  # add intercept
X_all = X_all.astype(float)  # Ensure all columns are float

# --- Case 2: Dropping ONE dummy variable (fixes the issue) ---
dummies_drop = pd.get_dummies(data["Title"], drop_first=True)
X_drop = pd.concat([data[["Experience"]], dummies_drop], axis=1)
X_drop = sm.add_constant(X_drop)
X_drop = X_drop.astype(float)  # Ensure all columns are float

# Split data into train and test sets (use same split for both cases)
X_all_train, X_all_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)
X_drop_train, X_drop_test, _, _ = train_test_split(X_drop, y, test_size=0.2, random_state=42)

# Fit models on training data
model_all = sm.OLS(y_train, X_all_train).fit()
print("Keeping ALL dummies (multicollinearity case):")
print(model_all.summary())

model_drop = sm.OLS(y_train, X_drop_train).fit()
print("\nDropping ONE dummy (correct way):")
print(model_drop.summary())

print("Train R^2 Score (all dummies):", r2_score(y_train, model_all.predict(X_all_train)))
print("Test R^2 Score (all dummies):", r2_score(y_test, model_all.predict(X_all_test)))
print("Train R^2 Score (drop one dummy):", r2_score(y_train, model_drop.predict(X_drop_train)))
print("Test R^2 Score (drop one dummy):", r2_score(y_test, model_drop.predict(X_drop_test)))
