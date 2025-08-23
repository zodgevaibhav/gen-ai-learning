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
import pickle

################### Data Load and Primary Analysis##################

df = pd.read_csv("iris.csv") 


############################ Data Cleansing ########################


encoder = LabelEncoder()
encoder.fit(df['species']) 
print(encoder.classes_ ) # Print all the classed that encoder found

# Print encoder class and respective encoded number. Might needed for mapping and putting value back
for class_label, encoded_label in enumerate(encoder.classes_):
    print(f"Class: {encoded_label}, Encoded as: {class_label}")


df['species'] = encoder.transform(df['species'])


############################ Data Visulization/Analysis ########################


print(df.corr())



############################ Split the data ########################
x = df.drop('species', axis=1)  # Features: all columns except 'species'
y = df['species']  # Target: 'species' column


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2131546)

############################ Create Model ########################
model = LogisticRegression()
model.fit(x_train, y_train) # Train the model using the training sets


############################ Save the model ########################

# Save the model into a pkl file

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)