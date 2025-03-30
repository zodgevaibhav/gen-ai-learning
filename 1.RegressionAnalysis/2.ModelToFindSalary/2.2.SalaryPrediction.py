import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the dataset from a CSV file
df = pd.read_csv("salary_data.csv")

# Separate the features (independent variables) and the target (dependent variable)
x = df.drop('Salary', axis=1)  # Features: all columns except 'Salary'
y = df['Salary']  # Target: 'Salary' column

# Initialize the Linear Regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x, y)

# Predict the salary for 15 years of experience
#salaries = model.predict([[15]])
salaries = model.predict(pd.DataFrame([[15]], columns=['Experience']))

# Print the predicted salary
print("Salary of 15 years of experience is:", salaries[0])
