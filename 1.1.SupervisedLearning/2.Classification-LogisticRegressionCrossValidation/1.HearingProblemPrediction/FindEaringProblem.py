import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib


df = pd.read_csv("hearing_test.csv")

# Exploratory Data Analysis (EDA)
# print("############# Columns : ")
# print(df.columns)
# print("############# Head : ")
# print(df.head())
# print("############# Tail : ")
# print(df.tail())
# print("############# Info : ")
# print(df.info())  # No need for print()

# print("############# Describe : ")
# print(df.describe())

print("############# Correlation : ")
print(df.corr())

# Split by category
positive = df[df["test_result"] == 1]
negative = df[df["test_result"] == 0]

# Scatter plot
plt.figure(figsize=(7,5))
plt.scatter(positive["age"], positive["physical_score"], 
            color="green", label="Test Result = 1", marker=".", s=80)
plt.scatter(negative["age"], negative["physical_score"], 
            color="red", label="Test Result = 0", marker=".", s=80)

plt.xlabel("Age")
plt.ylabel("Physical Score")
plt.title("Patient Data: Age vs Physical Score")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()


x = df.drop(columns=['test_result'], axis=1)
y = df['test_result']

# Split the data into training and testing sets
# 80% of the data will be used for training and 20% for testing
# random_state is used to ensure that the data is split in the same way every time
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=23123123)

# Build the model
model = LogisticRegression()

model.fit(x_train, y_train)  # Train the model using the training sets

output = model.predict(pd.DataFrame([[69,25]], columns=["age","physical_score"]))  # Predict for a new data point

print("Predicted Output for a 69 years old person with physical score of 25: ", output)

# Test the model
# Predict the test set results

y_pred = model.predict(x_test)

# Get the confustion matrix
# Confusion matrix is a table that is often used to describe the performance of a classification model
# It is a summary of the prediction results on a classification problem
# It shows the ways in which your classification model is confused when it makes predictions
# Confusion Matrix:
#    [[359  46]
#    [ 40 555]]
#    True Positive: 359
#    True Negative: 555
#    False Positive: 46
#    False Negative: 40
# This means, the model correctly predicted 359 positive cases and 555 negative cases.
# It incorrectly predicted 46 positive cases as negative and 40 negative cases as positive.

confusion = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(confusion)

# Get the accuricy score
# Accuracy Score:
#    0.914
# Accuracy is the ratio of correctly predicted instances to the total instances
# It is a measure of how often the classifier is correct
# Accuracy = (TP + TN) / (TP + TN + FP + FN)
# where TP = True Positive, TN = True Negative, FP = False Positive, FN = False Negative
# (359 + 555) / (359 + 555 + 46 + 40) = 0.914

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy Score:")
print(accuracy)