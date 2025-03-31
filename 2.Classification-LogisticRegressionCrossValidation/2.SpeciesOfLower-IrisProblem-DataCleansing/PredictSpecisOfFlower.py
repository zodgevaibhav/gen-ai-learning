# Author: Vaibhav Zodge
# Outcome: Learn Data Cleansing 
#          Model Evaluation using Confusion Matrix, Precision, F1 Score

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, f1_score, classification_report

################### Data Load and Primary Analysis##################

df = pd.read_csv("iris.csv") 
# # Read first few records
# print("############# Head : ")
# print(df.head())
# # Read last few records
# print("############# Tail : ")
# print(df.tail())


# # Get some basic information about the dataset
# print("############# Info : ")
# print(df.info())  # No need for print()

############################ Data Cleansing ########################

# On basic info will see species is textual and not numeric
# So we need to convert the species into numeric
# Label encoding is a technique used to convert categorical variables into numerical values
# It assigns a unique integer to each category in the variable
# For example, if we have a variable with three categories: 'red', 'green', and 'blue',
# label encoding would assign the values 0, 1, and 2 to these categories respectively
encoder = LabelEncoder()
encoder.fit(df['species']) # Fit the encoder to the species column 
                           # This will create a mapping of the unique values in the species column to integers
print(encoder.classes_ )

df['species'] = encoder.transform(df['species']) # Transform the species column
                                                 # This will replace the original values in the species column with their corresponding integer values
##   OR use below method which fit and transform in one step
# df['species'] = encoder.fit_transform(df['species']) # Transform the species column

print("############# Info : ")
df.info()  # No need for print()

############################ Data Visulization/Analysis ########################

#plt.scatter(df['sepal_length'], df['species'])
#plt.show()
# We will observe data visualization is not helpful because data is categorical data and not linear data
# Categorical data is not linear data, meaning it does not follow a straight line. 
# Categorical data is often represented as discrete values or categories, rather than continuous values.

print(df.corr())

#              sepal_length  sepal_width  petal_length  petal_width   species
#sepal_length      1.000000    -0.109369      0.871754     0.817954  0.782561
#sepal_width      -0.109369     1.000000     -0.420516    -0.356544 -0.419446
#petal_length      0.871754    -0.420516      1.000000     0.962757  0.949043
#petal_width       0.817954    -0.356544      0.962757     1.000000  0.956464
#species           0.782561    -0.419446      0.949043     0.956464  1.000000
# The correlation matrix shows the correlation coefficients between different features in the dataset.
# The values range from -1 to 1, where: 1 indicates a perfect positive correlation, -1 indicates a perfect negative correlation,

# Analysis of correlation:
    # Strong correlations:
    # - petal_length and petal_width (0.962757)
    # - petal_length and species (0.949043)
    # - petal_width and species (0.956464)
    # - sepal_length and petal_length (0.871754)
    # - sepal_length and petal_width (0.817954)
    # - sepal_length and species (0.782561)

    # Weak correlations:
    # - sepal_length and sepal_width (-0.109369)
    # - sepal_width and petal_length (-0.420516)
    # - sepal_width and petal_width (-0.356544)
    # - sepal_width and species (-0.419446)

############################ Split the data ########################
x = df.drop('species', axis=1)  # Features: all columns except 'species'
y = df['species']  # Target: 'species' column

# Split the data into training and testing sets
# 80% of the data will be used for training and 20% for testing
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2131546)

############################ Create Model ########################
model = LogisticRegression()
model.fit(x_train, y_train) # Train the model using the training sets
# Test the model
y_pred = model.predict(x_test)
print("Predicted Species: ", y_pred)
print("Actual Species: ", y_test.values)


############################ Model Evaluations/Metrics ########################

print("############# Accuracy : ")
print(accuracy_score(y_test, y_pred)) # Accuracy of the model
print("############# Confusion Matrix : ")
print(confusion_matrix(y_test, y_pred)) # Confusion matrix of the model
# The confusion matrix is a table that is often used to describe the performance of a classification model

# Precision is the ratio of true positive predictions to the total number of positive predictions made by the model
# Which means how many of the predicted positive cases were actually positive
# Precision = TP / (TP + FP), where TP is true positives and FP is false positives
# average : {'micro', 'macro', 'samples', 'weighted'}
# micro : Calculate metrics globally by counting the total true positives, false negatives and false positives.
# macro : Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
# samples : Calculate metrics for each instance, and find their average (only meaningful for multilabel classification).
# weighted : Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label).
precision = precision_score(y_test, y_pred, average='weighted')
print("############# Precision : ") 
print(precision) # Precision of the model

# F1 score is the harmonic mean of precision and recall
# F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
# F1 Score is a measure of a model's accuracy on a dataset
# It is the weighted average of precision and recall
# F1 Score is a good measure of a model's performance when the class distribution is imbalanced
# F1 Score is a better measure than accuracy for imbalanced datasets
f1Score = f1_score(y_test, y_pred, average='weighted')
print("############# F1 Score : ")
print(f1Score) # F1 Score of the model


print("############# Classification Report : ")
print(classification_report(y_test, y_pred)) # Classification report of the model
# The classification report is a summary of the precision, recall, F1 score, and support for each class in the dataset
# The classification report is a useful tool for evaluating the performance of a classification model
# It provides a detailed breakdown of the model's performance for each class in the dataset
# The classification report includes the following metrics:
# - precision: The ratio of true positive predictions to the total number of positive predictions made by the model
# - recall: The ratio of true positive predictions to the total number of actual positive cases in the dataset
# - f1-score: The harmonic mean of precision and recall
# - support: The number of actual occurrences of the class in the specified dataset

############################ Result Visualiation ########################

# identify the records for setosa (0)
plt.scatter(x_test['sepal_length'][y_pred==0], x_test['sepal_width'][y_pred==0], color='red', label='Setosa')

# identify the records for versicolor (1)
plt.scatter(x_test['sepal_length'][y_pred == 1], x_test['sepal_width'][y_pred == 1], color="green", label="versicolor")

# identify the records for virginica (2)
plt.scatter(x_test['sepal_length'][y_pred == 2], x_test['sepal_width'][y_pred == 2], color="blue", label="virginica")

plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Iris Species Classification')
plt.legend()
plt.show()