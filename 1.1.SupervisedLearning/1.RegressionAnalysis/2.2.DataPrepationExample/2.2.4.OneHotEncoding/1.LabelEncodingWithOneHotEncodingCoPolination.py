import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("salary_data.csv")

X = df.drop("Salary", axis=1)
y = df["Salary"]

label_encoder_title = LabelEncoder()
X_label_encoded = X.copy()
X["Title"] = label_encoder_title.fit_transform(X["Title"])

column_transformer = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(sparse_output=False, drop="first"), ["Title"])
    ],
    remainder="passthrough"  # keep other columns as it is
)

X = column_transformer.fit_transform(X)
X = pd.DataFrame(X, columns=column_transformer.get_feature_names_out())

#print("One-Hot Encoded Data:\n", X.head(), "\n")

model = LinearRegression()
model.fit(X, y)
# Prepare new data for prediction
data_to_predict = pd.DataFrame([["Project Manager", 5]], columns=["Title", "Experience"])
data_to_predict["Title"] = label_encoder_title.transform(data_to_predict["Title"])
new_data_transformed = column_transformer.transform(data_to_predict)

y_pred = model.predict(pd.DataFrame(new_data_transformed,columns=column_transformer.get_feature_names_out()))
print(y_pred)
