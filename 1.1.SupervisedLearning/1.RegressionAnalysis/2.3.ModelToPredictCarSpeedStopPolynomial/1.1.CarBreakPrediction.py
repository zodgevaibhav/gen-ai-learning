import pandas as pd
import matplotlib
import matplotlib.pyplot as ply
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

matplotlib.use("Agg")  # avoids GUI state messages

df = pd.read_csv('data.csv')

# df.info()

corr = df['Speed'].corr(df['BrakingDistance'])
# print(corr)

x = df.drop(columns=['BrakingDistance'], axis=1)
y=df['BrakingDistance']

# print(x)

poly = PolynomialFeatures(degree=2)
x_square = poly.fit_transform(x) 
# print(x_square)

model = LinearRegression()
model.fit(x_square, y)
output = model.predict(poly.transform([[120]]))

print("Braking distance at speed 120 is : " )
print(output)

ply.plot(df['Speed'], df['BrakingDistance'])
ply.xlabel('Speed')
ply.ylabel('BrakingDistance')
ply.title('Speed vs BrakingDistance')
# ply.show()

# 617*617 = 380689