# Mall Customers Segmentation with PCA + KMeans
# Author : Vaibhav Zodge

# PCA (Principal Component Analysis)
# Projects data into fewer “principal components” that capture maximum variance.
# Example: 100 features → reduce to 2 or 3 while keeping 90–95% of the information.
# Use case: Customer data with income, spending, age, etc., reduced to 2D for visualization.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# -------------------------
# Load and prepare dataset
# -------------------------
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender"], axis=1)   # Keep Age also for PCA
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

# -------------------------
# Step 1: Standardize the data
# -------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# -------------------------
# Step 2: Apply PCA (reduce to 2 components for visualization)
# -------------------------
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Create a DataFrame with PCA results
pca_df = pd.DataFrame(pca_data, columns=['PC1', 'PC2'])

# -------------------------
# Step 3: Apply KMeans clustering on PCA data
# -------------------------
kmeans = KMeans(n_clusters=5, random_state=123)
pca_df['Cluster'] = kmeans.fit_predict(pca_df)

# -------------------------
# Step 4: Visualization
# -------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=pca_df, palette='Set2', s=100)
plt.title("Customer Segmentation using PCA + KMeans")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

# -------------------------
# Step 5: Check explained variance
# -------------------------
print("Explained variance ratio (information retained by each component):")
print(pca.explained_variance_ratio_)
print("Total information retained:", np.sum(pca.explained_variance_ratio_))
