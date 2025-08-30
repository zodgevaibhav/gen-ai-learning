
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("SpendingData.csv")
X = data.drop("Spendings", axis=1)
y = data["Spendings"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("X_train:\n", X_train.head(), "\n")
print("X_test:\n", X_test.head(), "\n")
print("y_train:\n", y_train.head(), "\n")
print("y_test:\n", y_test.head(), "\n")