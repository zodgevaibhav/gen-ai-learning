import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load the model from pickle file
# rb = read binary
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

salaries = model.predict(pd.DataFrame([[15]], columns=['Experience']))

# Print the predicted salary
print("Salary of 15 years of experience is:", salaries)
