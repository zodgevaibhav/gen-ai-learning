import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load the dataset from a CSV file
df = pd.read_csv("salary_data.csv")

# Separate the features (independent variables) and the target (dependent variable)
x = df.drop('Salary', axis=1) 
y=df['Salary']

# Initialize the Linear Regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x,y)

# Since we have model which is trained, we can plot the BEST FIT REGRESSION LINE
plt.scatter(df['Experience'], df['Salary'],label='Observed Data')
plt.scatter(df['Experience'], model.predict(x), color='blue',label='Predicted Data')
plt.plot(df['Experience'], model.predict(x), color='red',label='Best Fit Line')
plt.legend()
plt.show()  

# Understand how model is bullt (internal formula)
# y = mx + c
# y = dependent variable
# x = independent variable
# m = coefficient
# c = intercept
# y = mx + c
# y = model.coef_ * x + model.intercept_
# y = model.coef_ * 15 + model.intercept_
# y = model.coef_[0] * 15 + model.intercept_ # Since model.coef_ is 1D array
# yearExperience = 15
# salary = model.coef_[0] * yearExperience + model.intercept_
# print("Salary of 15 years of experience is:", salary)