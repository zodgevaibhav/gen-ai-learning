import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("salary_data.csv")

X = df.drop("Salary", axis=1)
y = df["Salary"]

# One-Hot Encode Title directly
column_transformer = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(sparse_output=False, drop="first"), ["Title"])
    ],
    remainder="passthrough"
)

X_transformed = column_transformer.fit_transform(X)
X_transformed = pd.DataFrame(X_transformed, columns=column_transformer.get_feature_names_out())

model = LinearRegression()

print(X_transformed.head())
model.fit(X_transformed, y)

# Predict new data
data_to_predict = pd.DataFrame([["Project Manager", 5]], columns=["Title", "Experience"])
new_data_transformed = column_transformer.transform(data_to_predict)
new_data_transformed = pd.DataFrame(new_data_transformed, columns=column_transformer.get_feature_names_out())
print(new_data_transformed)
y_pred = model.predict(new_data_transformed)
print(y_pred)
