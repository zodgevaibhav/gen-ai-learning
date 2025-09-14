
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data = pd.read_csv("../SpendingData.csv")
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

# when we we give x1 data and then predicted value is y1
# then difference between y1 and y is error
# x= 24, y=36508
# model.pridict([[24]]) = 36000 
# error = 36508-36000 = 508
# Score is summation of all error & how well model is performing
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

#   1.0 → Perfect predictions. (Could be overfitting) : Near to 1 is better
#   0.0 → Model is no better than predicting the mean.
#   < 0 → Model is worse than just predicting the mean.
# Small difference = good generalization.
# Large gap = investigate overfitting or underfitting.
print(f"Train R^2 Score: {train_score}")
print(f"Test R^2 Score: {test_score}")