import pandas as pd
from sklearn.experimental import enable_iterative_imputer # Why is this needed? Because IterativeImputer is still experimental and not part of the main API yet.
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge

# BayesianRidge is light weight and efficient, making it suitable for iterative imputation tasks.
df = pd.read_csv('salary_data.csv')

imputer = IterativeImputer(estimator=BayesianRidge(), max_iter=10, random_state=0)

df["salary"] = imputer.fit_transform(df[["Salary"]])

print("After Mean Imputation:\n", df, "\n")