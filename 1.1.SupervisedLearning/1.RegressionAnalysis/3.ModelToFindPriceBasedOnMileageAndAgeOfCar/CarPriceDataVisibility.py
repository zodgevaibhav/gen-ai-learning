import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle


df = pd.read_csv("car_price_data.csv")

#df.info()
print(df.columns)

print(df['Mileage'].corr(df['Price']))
print(df['Age'].corr(df['Price']))

# Data Scaling Example
# Scaling means transforming data to a specific range
# Two common techniques are Normalization and Standardization   
# MinMaxScaler (Normalization) : Scales data to a fixed range - usually 0 to 1
# StandardScaler (Standardization) : Scales data to have mean=0 and variance=1
## Which means it centers the data around 0 and scales it based on standard deviation
## Example : If mean=50 and std=10, then value 60 will be transformed to (60-50)/10 = 1

scaler = StandardScaler()
df[['Age','Mileage']] = scaler.fit_transform(df[['Age','Mileage']]) # Scaling only feature columns
print("Scaled Data:\n", df.head(), "\n")

plt.scatter( df['Price'],df['Age'])
plt.scatter(df['Price'],df['Mileage'])
plt.xlabel("Price")
plt.ylabel("Age/Mileage")
plt.show()

