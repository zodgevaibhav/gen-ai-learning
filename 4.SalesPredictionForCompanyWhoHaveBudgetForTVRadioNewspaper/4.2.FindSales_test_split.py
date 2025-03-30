# Author: Vaibhav Zodge
# Outcome: Model Testing
# We should test our model for the sales prediction
# To test the model, we should split our data into two parts, training and testing
# And then on the basis of Testing Data we try to predict the sales
# and see the error rate

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the dataset from a CSV file
df = pd.read_csv("Advertising.csv")

x = df.drop(['sales'], axis=1)  # Features: all columns except 'sales'
y = df['sales']  # Target: 'sales' column

# Split the data into training and testing sets
# 80% of the data will be used for training and 20% for testing
# random_state is used to ensure that the data is split in the same way every time
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=42)


# Build the model
model = LinearRegression()
model.fit(x_train, y_train) # Train the model using the training sets

# Test the model
sales = model.predict(pd.DataFrame([[100, 100,100]], columns=['TV', 'radio','newspaper']))
print("Sales for 100 TV, 100 Radio, 100 Newspaper is:", sales[0])
