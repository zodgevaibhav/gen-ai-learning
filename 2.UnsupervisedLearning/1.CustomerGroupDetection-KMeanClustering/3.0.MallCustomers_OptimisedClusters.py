# Mall Customers Segmentation
# Author : Vaibhav Zodge

# What Program Does : Customer Segmentation
    #The main goal is to divide mall customers into distinct groups (clusters) where each group contains customers with similar financial and spending characteristics.
    #    For example:
    #        One cluster might represent high-income, high-spending customers.
    #        Another might represent low-income, low-spending customers.

# What we learned :
    #1. Customer Segmentation
    #2. Find the Optimal Number of Groups/Clusters
    #3. Create Clusters
    #4. Visualize the Groups

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load and prepare the dataset
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender", "Age"], axis=1)
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

# Apply KMeans with chosen cluster count (e.g., 5)
# K - किती क्लस्टर???
# Mean -> Average
# Mean -> used inside to decide centroid :)
kmeans_final = KMeans(n_clusters=5, random_state=123)
df['Cluster'] = kmeans_final.fit_predict(df)

# Visualize clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Income', y='Spending', hue='Cluster', data=df, palette='Set2', s=100)
plt.title('Customer Segments by Income and Spending')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

