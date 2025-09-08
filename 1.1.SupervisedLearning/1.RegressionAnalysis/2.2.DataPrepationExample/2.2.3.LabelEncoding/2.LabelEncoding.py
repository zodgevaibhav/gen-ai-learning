import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

# Load data
data = pd.read_csv("salary_data_hard_encoding.csv")

X = data.drop("Salary", axis=1)
y = data["Salary"]

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(pd.DataFrame([[2,5]],columns=["Title","Experience"]))
print(y_pred)
