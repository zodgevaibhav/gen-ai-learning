import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


df = pd.read_csv("salary_data.csv")


plt.scatter(df['Experience'], df['Salary'])
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.title('Experience vs Salary')
plt.show()  # Uncomment to see graph

x = df.drop('Salary', axis=1) # We are usiong drop since independent variable should be two dimention array
y=df['Salary']

model = LinearRegression()

model.fit(x,y)

re_predict_all_x = model.predict(x)

# Since we have model which is trained, we can plot the BEST FIT REGRESSION LINE

plt.scatter(df['Experience'], df['Salary'],label='Observed Data')
plt.scatter(df['Experience'], re_predict_all_x, color='blue',label='Predicted Data')
plt.plot(df['Experience'], re_predict_all_x, color='red',label='Best Fit Line')
plt.legend()
plt.show()  # Uncomment to see graph
