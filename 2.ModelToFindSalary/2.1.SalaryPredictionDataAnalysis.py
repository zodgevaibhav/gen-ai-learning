import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# Load the dataset from a CSV file
df = pd.read_csv("salary_data.csv")

# Print dataset details
#print("############# Columns : ")
#print(df.columns)

#print("############# Info : ")
#df.info()  # No need for print()

#print("############# Describe : ")
#print(df.describe())


# Plot scatter graph
# Visualize the data
# A scatter plot is a graph that shows the relationship between two variables
# The x-axis represents one variable, and the y-axis represents the other
# Each point on the graph represents a single observation
# Scatter plots are used to see if there is a relationship between two variables
# Scatter plots are used to see if there is a correlation between two variables
# Scatter plots are used to see if there is a pattern between two variables
# Scatter plots are used to see if there is a trend between two variables

plt.scatter(df['Experience'], df['Salary'])
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.title('Experience vs Salary')
#plt.show()  # Uncomment to see graph

# Find covariance (Find is there any relation between two variables)
# Covariance is a measure of how much two variables change together
# Positive covariance means that the variables are directly proportional
# Negative covariance means that the variables are inversely proportional
# Zero covariance means that the variables are not related
# Covariance can be any value
# Covariance is not normalized,standardized,bounded,percentage,probability,correlation
## Covariance of x and y = Σ((x - mean(x)) * (y - mean(y))) / (n-1)
## Covariance of x = Covariance of y
##[[cov(x,y)]] = cov(x,x) = cov(y,y)
covariance = np.cov(df['Experience'], df['Salary'])
print("Covariance: ", covariance)

# Find correlation (Relation is stron ok)
# Correlation is a normalized form of covariance
# It is a measure of how much two variables change together
# Correlation ranges from -1 to 1
# 1 means that the variables are perfectly correlated
# 0 means that the variables are not correlated
# -1 means that the variables are perfectly inversely correlated
correlation = df['Experience'].corr(df['Salary'])
print("Correlation: ", correlation)

# Separate the features (independent variables) and the target (dependent variable)
# Why drop function ? : We are using drop since independent variable should be two dimention array
# Why x is 2D array ? : x is 2D array since it is independent variable
# Why axis=1 ? : axis=1 means we are dropping column
# Why axis=0 ? : axis=0 means we are dropping row
# Why x and y ? : x is independent variable and y is dependent variable as per convention
x = df.drop('Salary', axis=1) # We are usiong drop since independent variable should be two dimention array
y=df['Salary']

# Initialize the Linear Regression model
# Why Linear Regression ? : Linear regression is used for regression problems
# Regression is used to predict a continuous value
# Linear regression is used to predict a continuous value using one or more independent variables
# Linear regression is used to predict a continuous value using a linear equation
# Linear regression is used to predict a continuous value using a straight line
model = LinearRegression()

# Fit the model to the data
# Why x and y ? : x is independent variable and y is dependent variable as per convention
# model.fit is used to train the model
model.fit(x,y)

# Predict the salary for 15 years of experience
# Why model.predict ? : model.predict is used to predict the value
# Why pd.DataFrame ? : pd.DataFrame is used to create a data frame
# Why predict need DataFrame ? : predict need DataFrame to predict the value and it should be 2D array
# DataFrame is a 2D labeled data structure with columns of potentially different types
# It is generally the most commonly used pandas object
# Like an SQL table or Excel spreadsheet
salaries = model.predict(pd.DataFrame([[15]],columns=['Experience']))
print("Salary of 15 years of experience is:", salaries[0])

# Since we have model which is trained, we can plot the BEST FIT REGRESSION LINE

plt.scatter(df['Experience'], df['Salary'],label='Observed Data')
plt.scatter(df['Experience'], model.predict(x), color='blue',label='Predicted Data')
plt.plot(df['Experience'], model.predict(x), color='red',label='Best Fit Line')
plt.legend()
plt.show()  # Uncomment to see graph


# Understand how model is bullt (internal formula)
# y = mx + c
# y = dependent variable
# x = independent variable
# m = coefficient
# c = intercept
# y = mx + c
# y = model.coef_ * x + model.intercept_
# y = model.coef_ * 15 + model.intercept_
# y = model.coef_[0] * 15 + model.intercept_ // Since model.coef_ is 1D array
yearExperience = 15
salary = model.coef_[0] * yearExperience + model.intercept_
print("Salary of 15 years of experience is:", salary)