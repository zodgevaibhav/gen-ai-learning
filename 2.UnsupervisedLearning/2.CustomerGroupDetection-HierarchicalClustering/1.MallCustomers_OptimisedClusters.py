# Mall Customers Segmentation using Hierarchical Clustering
# Author : Vaibhav Zodge

# What Program Does : Customer Segmentation
# The main goal is to divide mall customers into distinct groups (clusters) 
# where each group contains customers with similar financial and spending characteristics.
# Example:
#   - One cluster might represent high-income, high-spending customers.
#   - Another might represent low-income, low-spending customers.

# What we learned :
#   1. Customer Segmentation
#   2. Find the Optimal Number of Groups/Clusters using Dendrogram
#   3. Create Clusters using Agglomerative Clustering
#   4. Visualize the Groups

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

# -------------------------
# Load and prepare dataset
# -------------------------
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender", "Age"], axis=1)
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

# -------------------------
# Step 1: Dendrogram (to decide number of clusters)
# -------------------------
plt.figure(figsize=(10, 6))
dendrogram = sch.dendrogram(sch.linkage(df, method='ward'))
plt.title('Dendrogram for Customer Segmentation')
plt.xlabel('Customers')
plt.ylabel('Euclidean distances')
plt.show()

# -------------------------
# Step 2: Fit Hierarchical Clustering model
# -------------------------
hc = AgglomerativeClustering(n_clusters=5, metric='euclidean', linkage='ward')
df['Cluster'] = hc.fit_predict(df)

# -------------------------
# Step 3: Visualize clusters
# -------------------------
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Income', y='Spending', hue='Cluster', data=df, palette='Set1', s=100)
plt.title('Customer Segments by Income and Spending (Hierarchical Clustering)')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

# -------------------------
# Step 4: Predict for new customers (example: Income=60, Spending=50)
# -------------------------
# Note: AgglomerativeClustering does not have a direct .predict() like KMeans.
# To assign new points, we must compare them to cluster centroids manually.
# For simplicity, here we show which cluster the training data [60,50] belongs to:

from sklearn.metrics import pairwise_distances_argmin_min

# Get cluster centers manually
cluster_centers = df.groupby('Cluster')[['Income','Spending']].mean().values

# Predict new point's cluster
new_points = np.array([[60, 50], [80, 70]])
closest_clusters, _ = pairwise_distances_argmin_min(new_points, cluster_centers)

print("New points:", new_points)
print("Predicted clusters:", closest_clusters)
