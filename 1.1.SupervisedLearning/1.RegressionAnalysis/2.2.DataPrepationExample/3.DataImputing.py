# Data Imputing Example
# Imputing means filling missing values with some strategy
# Strategies: mean, median, most_frequent, constant
# Mean Imputation : Mean meaning average of all values
# Median Imputation : Median meaning middle value of all values
# Most Frequent Imputation : Most Frequent meaning value which is most repeated
# Constant Imputation : Constant meaning value which we provide

import pandas as pd
from sklearn.impute import SimpleImputer

# Sample data
df = pd.DataFrame({
    "age": [20, 30, None, 50],
    "salary": [50000, None, 70000, 80000]
})

# mean, median, most_frequent, constant
# Mean Imputation : Mean meaning average of all values
# Median Imputation : Median meaning middle value of all values
# Most Frequent Imputation : Most Frequent meaning value which is most repeated
# Constant Imputation : Constant meaning value which we provide
# Mean
mean_df = df.copy()
imputer = SimpleImputer(strategy="mean") 
mean_df["age"] = imputer.fit_transform(mean_df[["age"]])
mean_df["salary"] = imputer.fit_transform(mean_df[["salary"]])
print("After Mean Imputation:\n", mean_df, "\n")

# Median
median_df = df.copy()
imputer = SimpleImputer(strategy="median") 
median_df["age"] = imputer.fit_transform(median_df[["age"]])
median_df["salary"] = imputer.fit_transform(median_df[["salary"]])
print("After Median Imputation:\n", median_df, "\n")

# Most Frequent
freq_df = df.copy()
imputer = SimpleImputer(strategy="most_frequent") 
freq_df["age"] = imputer.fit_transform(freq_df[["age"]])
freq_df["salary"] = imputer.fit_transform(freq_df[["salary"]])
print("After Most Frequent Imputation:\n", freq_df, "\n")

# Constant
const_df = df.copy()
imputer = SimpleImputer(strategy="constant", fill_value=0) 
const_df["age"] = imputer.fit_transform(const_df[["age"]])
const_df["salary"] = imputer.fit_transform(const_df[["salary"]])
print("After Constant Imputation:\n", const_df, "\n")