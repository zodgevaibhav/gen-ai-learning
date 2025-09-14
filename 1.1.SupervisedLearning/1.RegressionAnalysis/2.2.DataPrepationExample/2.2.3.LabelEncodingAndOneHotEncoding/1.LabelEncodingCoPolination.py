import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

df = pd.read_csv("salary_data.csv")

X = df.drop("Salary", axis=1)
y = df["Salary"]

label_encoder_title = LabelEncoder()
X_label_encoded = X.copy()
X["Title"] = label_encoder_title.fit_transform(X["Title"])

# for i, item in enumerate(label_encoder_title.classes_):
#     print(f"Label {i} is for {item}")


model = LinearRegression()
model.fit(X, y)

encoded_title_to_predict = label_encoder_title.transform(["Project Manager"])

y_pred = model.predict(pd.DataFrame([[encoded_title_to_predict,5]],columns=["Title","Experience"]))
print(y_pred)
