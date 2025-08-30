# numpy helps to do mathematical calculations for scientific, numeric, data-intensive
import numpy as np
# pandas helps to handle data in tabular form (rows and columns)
import pandas as pd
import matplotlib.pyplot as plt



# Load the dataset from a CSV file
# Data Frame is a 2D labeled data structure with columns of potentially different types
# It is generally the most commonly used pandas object
# Like an SQL table or Excel spreadsheet
df = pd.read_csv("salary_data.csv")

# Print dataset details
#print("############# Columns : ")
print(df.columns)

#print("############# Info : ")
df.info()  # No need for print()

#print("############# Describe : ")
print(df.describe())

# Mean, Median, Mode
# Mean is the average of all values
# Median is the middle value when all values are sorted
# Mode is the most frequently occurring value
# Mean, Median, Mode are used to understand the distribution of data
print("Mean Salary: ", df['Salary'].mean())
print("Median Salary: ", df['Salary'].median())
print("Mode Salary: ", df['Salary'].mode()[0])

# Plot scatter graph
# Visualize the data
# A scatter plot is a graph that shows the relationship between two variables
# The x-axis represents one variable, and the y-axis represents the other
# Each point on the graph represents a single observation
# Scatter plots are used to see if there is a relationship between two variables
# Scatter plots are used to see if there is a correlation between two variables
# Scatter plots are used to see if there is a pattern between two variables
# Scatter plots are used to see if there is a trend between two variables
plt.scatter(df['Experience'], df['Salary'])
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.title('Experience vs Salary')
plt.show()  # Uncomment to see graph


# Find correlation (Relation is strong or weak between two variables)
# Correlation is a normalized form of covariance
# It is a measure of how much two variables change together
# Correlation ranges from -1 to 1
# 1 means that the variables are perfectly correlated
# 0 means that the variables are not correlated
# -1 means that the variables are perfectly inversely correlated
correlation = df['Experience'].corr(df['Salary'])
print("Correlation: ", correlation)


# Find covariance (Find is there any relation between two variables)
# Covariance is a measure of how much two variables change together
# Positive covariance means that the variables are directly proportional
# Negative covariance means that the variables are inversely proportional
# Zero covariance means that the variables are not related
# Covariance can be any value
# Covariance is not normalized,standardized,bounded,percentage,probability,correlation
## Covariance of x and y = Σ((x - mean(x)) * (y - mean(y))) / (n-1)
## Covariance of x = Covariance of y
##[[cov(x,y)]] = cov(x,x) = cov(y,y)
covariance = np.cov(df['Experience'], df['Salary'])
print("Covariance: ", covariance)

