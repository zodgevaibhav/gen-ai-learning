import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the dataset from a CSV file
df = pd.read_csv("Advertising.csv")
#print(df.head())

# Exploratoring Data Analysis (EDA )
#print("############# Columns : ")
#print(df.columns)

# Read first few records
#print("############# Head : ")
#print(df.head())

# Read last few records
#print("############# Tail : ")
#print(df.tail())

# Get some basic information about the dataset
#print("############# Info : ")
#df.info()  # No need for print()

# Get statistical information about the dataset
#print("############# Describe : ")
#print(df.describe())

# Visualize the data
# A scatter plot is a graph that shows the relationship between two variables
# The x-axis represents one variable, and the y-axis represents the other
# Each point on the graph represents a single observation

## Relationship between TV and Sales seems not good relation
plt.scatter(df['TV'], df['sales'])
plt.xlabel('TV')
plt.ylabel('sales')
plt.title('TV vs Sales')
plt.show()  # Uncomment to see graph

## Relationship between TV and Radio seems not good relation
plt.scatter(df['radio'], df['sales'])
plt.xlabel('TV')
plt.ylabel('radio')
plt.title('Radio vs Sales')
plt.show()  # Uncomment to see graph

## Relationship between TV and News paper seems not good relation
plt.scatter(df['newspaper'], df['sales'])
plt.xlabel('newspaper')
plt.ylabel('newspaper')
plt.title('newspaper vs Sales')
plt.show()  # Uncomment to see graph

# Find the corelation coefficient
correlation = df.corr()
#print("Correlation between TV and Sales: ")
#print(correlation)

# Create independent variables
x = df.drop(['sales'], axis=1)  # Features: all columns except 'sales'
# x = x.drop('newspaper', axis=1)  #This can be also done
y = df['sales']  # Target: 'sales' column

# Build the model
model = LinearRegression()
model.fit(x, y) # x is independent variable and y is dependent variable   

# Test the model
sales = model.predict(pd.DataFrame([[100, 100,100]], columns=['TV', 'radio','newspaper']))
print("Sales for 100 TV, 100 Radio, 100 Newspaper is:", sales[0])
sales = model.predict(pd.DataFrame([[147, 23,19]], columns=['TV', 'radio','newspaper']))
print("Sales for 147 TV, 23 Radio, 19 Newspaper is:", sales[0])

## Some time some independent data might not found much relevant
## We should drop that data to get better prediction and speed
x = df.drop(['sales','newspaper'], axis=1)
y = df['sales']
model.fit(x, y)
sales = model.predict(pd.DataFrame([[100, 100]], columns=['TV', 'radio']))
print("Sales for 100 TV, 100 Radio is:", sales[0])
sales = model.predict(pd.DataFrame([[147, 23]], columns=['TV', 'radio']))
print("Sales for 147 TV, 23 Radio is:", sales[0])