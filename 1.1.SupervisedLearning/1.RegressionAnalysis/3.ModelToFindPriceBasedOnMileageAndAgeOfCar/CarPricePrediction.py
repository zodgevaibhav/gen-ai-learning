import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv("car_price_data.csv")

df.info()

print(df['Mileage'].corr(df['Price']))
print(df['Age'].corr(df['Price']))

plt.scatter(df['Price'], df['Age'])
plt.legend(['Age vs Price'])
plt.xlabel("Price")
plt.ylabel("Age")
plt.show()

plt.scatter(df['Price'], df['Mileage'])
plt.legend(['Mileage vs Price'])
plt.xlabel("Price")
plt.ylabel("Mileage")
plt.show()

# Separate the features (independent variables) and the target (dependent variable)
x = df.drop('Price', axis=1)  # Features: all columns except 'Price'
y = df['Price']  # Target: 'Price' column

model = LinearRegression()
model.fit(x, y)

predictions = model.predict(pd.DataFrame([[2,20000]],columns=['Age','Mileage']))
print(predictions)