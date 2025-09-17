
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

data = pd.read_csv("SpendingData.csv")
X = data.drop("Spendings", axis=1)
y = data["Spendings"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10000)

plt.scatter(X_train["Salary"], y_train, color='blue', label='Training data')
plt.scatter(X_test["Salary"], y_test, color='red', label='Testing data')
plt.xlabel("Salary")
plt.ylabel("Spendings")
plt.title("Train-Test Data Split")
plt.legend()
#plt.show()

model = LinearRegression()
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

#   1.0 → Perfect predictions. (Could be overfitting) : Near to 1 is better
#   0.0 → Model is no better than predicting the mean.
#   < 0 → Model is worse than just predicting the mean.
# Small difference = good generalization.
# Large gap = investigate overfitting or underfitting.
# R2 = 1 - (SS_res / SS_tot)
# This literally means:
    # R2 = 1 - (Sum of squares of residuals / Total sum of squares)
    # SS_res logic is to measure how far the predicted values are from the actual values.
        # so we take the difference between actual and predicted values, square them, and sum them up.
    # SS_tot logic is to measure how far the actual values are from the mean of actual values.
        # so we take the difference between actual values and mean (average) of actual values, square them,
        # and sum them up.
    # R2 score is total difference between actual and predicted values relative to the total difference between actual values and average of actual values.
# SS_res = Σ(yi - f(xi))^2
    # where f(xi) is the predicted value
    # yi is the actual value
    # We do square because if we get negative values, they will cancel out positive values.
# SS_tot = Σ(yi - ȳ)^2
    # where ȳ is the mean of the actual values
    # yi is the actual value

print(f"Train R^2 Score: {train_score}")
print(f"Test R^2 Score: {test_score}")


# --- Mean Absolute Error (MAE) ---
# Average of all positive (making square of then) differences between "actual and predicted values"
# Absolute meaning no negative values
mae = mean_absolute_error(y_test, y_pred)

# --- Mean Squared Error (MSE) ---
# Average of squared differences between actual and predicted values
mse = mean_squared_error(y_test, y_pred)

# --- Root Mean Squared Error (RMSE) ---
# Square root of MSE, interpretable in original units
rmse = np.sqrt(mse)

# --- Mean Absolute Percentage Error (MAPE) ---
# Expresses error as percentage of actual values
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100