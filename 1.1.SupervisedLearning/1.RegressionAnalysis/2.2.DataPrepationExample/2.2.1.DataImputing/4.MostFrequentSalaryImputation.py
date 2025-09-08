import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_csv('salary_data.csv')

imputer = SimpleImputer(strategy="most_frequent")

df["Salary"] = imputer.fit_transform(df[["Salary"]])

print("After Mean Imputation:\n", df, "\n")