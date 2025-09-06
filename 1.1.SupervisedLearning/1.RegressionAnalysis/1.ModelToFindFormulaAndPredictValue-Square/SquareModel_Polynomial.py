import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Load the dataset safely
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("Error: data.csv not found!")
    exit()

# # Print dataset details
# print("############# Columns : ")
# print(df.columns)

# print("############# Info : ")
# print(df.info())  # No need for print()

# print("############# Describe : ")
# print(df.describe())  # No need for print()

# Ensure required columns exist
if 'a' not in df.columns or 'b' not in df.columns:
    print("Error: Columns 'a' or 'b' not found in dataset")
    exit()

# Plot scatter graph or "Visualize the data"
print("############# Plot Graph : ")
plt.scatter(df['a'], df['b'])
plt.xlabel('a - Number')
plt.ylabel('b - Square of a')
plt.title('Number vs Square of Number')
#plt.show()  # Uncomment to see graph


corr = df['a'].corr(df['b'])
print("Correlation between a and b:", corr)

print("\n------------------------------------\n\n")
# Create and train the model
############# Create object of model"
model = LinearRegression()

X = df[['a']]  # Ensure X is a 2D array
y = df['b']

# Why we need PolynomialFeatures?
# Because our data is not linear, it's quadratic (b = a^2)
# We need to transform our features to include polynomial terms
# This will help the linear regression model to fit a non-linear relationship
# For example, if a = 3, we want to include a^2 = 9 as a feature
# So that the model can learn the relationship between a and b
# Without this transformation, the model will try to fit a straight line
# to the data, which will not work well for quadratic data
poly = PolynomialFeatures(degree=2,include_bias=False)  # Since b = a², we use degree=2
a_poly = poly.fit_transform(X)
# print("##### Transformed features : ")
# print(a_poly)

# print("##### Train the model")
model.fit(a_poly, df['b'])

# # Predict the square of 12
# print("##### Predict the square")
a_test = poly.transform(pd.DataFrame([[12]],columns=['a']))
square_predict = model.predict(a_test)
print("Square of 12 is:", square_predict[0])

