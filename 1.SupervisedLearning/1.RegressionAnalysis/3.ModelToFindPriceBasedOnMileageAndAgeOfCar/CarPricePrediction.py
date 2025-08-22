import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("car_price_data.csv")

# Separate the features (independent variables) and the target (dependent variable)
x = df.drop('Price', axis=1)  # Features: all columns except 'Price'
y = df['Price']  # Target: 'Price' column

model = LinearRegression()
model.fit(x, y)

predictions = model.predict(pd.DataFrame([[2,20000]],columns=['Age','Mileage']))
print(predictions)
predictions = model.predict([[2,20000]])
print(predictions)