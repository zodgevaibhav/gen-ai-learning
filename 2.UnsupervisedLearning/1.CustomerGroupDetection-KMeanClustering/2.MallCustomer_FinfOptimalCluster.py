import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load and prepare the dataset
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender", "Age"], axis=1)
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

wss = []  # Within-Cluster Sum of Squares
clusters_range = range(1, 11) # 10 clusters

for k in clusters_range: # for each k value
    model = KMeans(n_clusters=k, random_state=123) # create KMeans model    k =10
    model.fit(df) 
    wss.append(model.inertia_) # Intertia/WSS: Sum of squared distances to closest cluster center

# Plot Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(clusters_range, wss, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WSS (Inertia)')
plt.grid(True)
plt.show()

# 4/5