import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Load data
df = pd.read_csv('data.csv')
# df.info()

# Correlation
corr = df['Speed'].corr(df['BrakingDistance'])
# print("Correlation between Speed and BrakingDistance:", corr)

# Features & target
X = df[['Speed']]   # keep as DataFrame for sklearn
y = df['BrakingDistance']

# Create pipeline (PolynomialFeatures + LinearRegression)
degree = 2
model = make_pipeline(PolynomialFeatures(degree), LinearRegression())

# Fit model
model.fit(X, y)

# Predict braking distance at speed = 120
output = model.predict(pd.DataFrame([[120]],columns=['Speed']))
print("Braking distance at speed 120 is:", output[0])
