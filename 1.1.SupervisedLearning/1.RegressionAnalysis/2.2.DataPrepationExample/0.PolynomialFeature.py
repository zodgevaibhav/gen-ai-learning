import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Data
age = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
car_value = np.array([9.0, 8.5, 7.0, 5.0, 3.5, 2.0])

# Polynomial Features
poly = PolynomialFeatures(degree=2)  # you can try degree=3 for sharper curve
age_poly = poly.fit_transform(age)

# Fit Polynomial Regression
model = LinearRegression()
model.fit(age_poly, car_value)


age_range_poly = poly.transform(age)
car_pred = model.predict( poly.transform(age))

# Plotting
plt.figure(figsize=(8,5))
plt.plot(age, car_value, '-', label='Original Data', color='red')
plt.plot(age, car_pred, '-', label='Polynomial Fit', color='blue')
plt.title("Car Value Depreciation with Age")
plt.xlabel("Age (Years)")
plt.ylabel("Car Value (₹ Lakhs)")
plt.grid(True)
plt.legend()
plt.show()
