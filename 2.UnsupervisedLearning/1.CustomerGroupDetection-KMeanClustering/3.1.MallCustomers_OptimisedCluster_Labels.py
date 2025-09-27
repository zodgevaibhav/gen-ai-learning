import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# -------------------------------
# Load and prepare the dataset
# -------------------------------
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender", "Age"], axis=1)
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

# -------------------------------
# Apply final KMeans with K=5
# -------------------------------
kmeans_final = KMeans(n_clusters=5, random_state=123)
df['Cluster'] = kmeans_final.fit_predict(df)

# -------------------------------
# Get cluster centroids
# -------------------------------
centroids = kmeans_final.cluster_centers_
print("Cluster Centers (Income, Spending):")
print(centroids)

# -------------------------------
# Assign descriptive labels
# -------------------------------

cluster_labels = {
    0: "Budget-Conscious",      # Low income, low spending
    1: "Impulsive Spenders",    # Low income, high spending
    2: "Savers",                # High income, low spending
    3: "Premium Spenders",      # High income, high spending
    4: "Average Customers"      # Middle group
}

df['ClusterLabel'] = df['Cluster'].map(cluster_labels)

# -------------------------------
# Print sample with labels
# -------------------------------
print("\nSample customers with cluster labels:")
print(df.head(10))

# -------------------------------
# Predict new customers
# -------------------------------
new_customers = [[20, 20], [20, 80], [80, 20], [80, 80]]
pred_clusters = kmeans_final.predict(new_customers)

# Map to human labels
pred_labels = [cluster_labels[c] for c in pred_clusters]

print("\nPredictions for new customers (Income, Spending):")
for point, cid, lbl in zip(new_customers, pred_clusters, pred_labels):
    print(f"{point} -> Cluster {cid} ({lbl})")

# -------------------------------
# Visualize clusters
# -------------------------------
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Income', y='Spending', hue='ClusterLabel', data=df, palette='Set2', s=100)
plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=200, alpha=0.6, marker='X', label="Centroids")
plt.title('Customer Segments by Income and Spending')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()
