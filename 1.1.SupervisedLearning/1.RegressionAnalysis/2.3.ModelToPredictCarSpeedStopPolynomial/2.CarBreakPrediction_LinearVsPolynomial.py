import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Training Data
df = pd.read_csv('data.csv')

X = df.drop(columns=['BrakingDistance'],axis = 1)
y = df['BrakingDistance']

# Linear Regression (straight line)
lin_reg = LinearRegression()
lin_reg.fit(X, y)
y_pred_linear = lin_reg.predict(X)

# Polynomial Regression (degree=2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
poly_reg = LinearRegression()
poly_reg.fit(X_poly, y)
y_pred_poly = poly_reg.predict(X_poly)

# Plot the prediction by Linear and Polynomial Regression
plt.scatter(X, y, color="blue", label="Data points")
plt.plot(X, y_pred_linear, color="red", label="Linear Regression (straight line)")
plt.plot(X, y_pred_poly, color="green", label="Polynomial Regression (curve)")
plt.legend()
plt.xlabel("X")
plt.ylabel("y")
plt.title("Linear vs Polynomial Regression")
plt.show()
