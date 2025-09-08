import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 0: Create dataset
data = pd.read_csv('SalarySpendingMLImputation.csv')
print("Original Data:\n", data)

# ==============================
# STEP 1: TRAIN MODEL TO PREDICT SALARY
# ==============================

# 1a. Separate data into known and unknown salaries
known_salary = data[data["Salary"].notnull()]
unknown_salary = data[data["Salary"].isnull()]

# 1b. Train a model on Age -> Salary
X_salary = known_salary[["Age"]]
y_salary = known_salary["Salary"]

salary_model = LinearRegression()
salary_model.fit(X_salary, y_salary)

# 1c. Predict missing salaries
predicted_salaries = salary_model.predict(unknown_salary[["Age"]])

# 1d. Fill missing salaries
data.loc[data["Salary"].isnull(), "Salary"] = predicted_salaries
print("\nData after Salary Imputation:\n", data)

# ==============================
# STEP 2: TRAIN MODEL TO PREDICT SPENDING
# ==============================

X = data[["Age", "Salary"]]
y = data["Spending"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

spending_model = LinearRegression()
spending_model.fit(X_train, y_train)

# Predictions
y_pred = spending_model.predict(X_test)

print("\nPredicted Spending:", y_pred)
print("Actual Spending   :", list(y_test))

# Evaluation
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
