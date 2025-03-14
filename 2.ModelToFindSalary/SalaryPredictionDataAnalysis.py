import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


df = pd.read_csv("salary_data.csv")

# Print dataset details
#print("############# Columns : ")
#print(df.columns)

#print("############# Info : ")
#df.info()  # No need for print()

#print("############# Describe : ")
#print(df.describe())


# Plot scatter graph
#print("############# Plot Graph : ")
plt.scatter(df['Experience'], df['Salary'])
plt.xlabel('a - Number')
plt.ylabel('b - Square of a')
plt.title('Number vs Square of Number')
#plt.show()  # Uncomment to see graph

x = df.drop('Salary', axis=1) # We are usiong drop since independent variable should be two dimention array
y=df['Salary']

model = LinearRegression()

model.fit(x,y)

salaries = model.predict(pd.DataFrame([[13]],columns=['Experience']))
print("Salary of 15 years of experience is:", salaries[0])
