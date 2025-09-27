
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# 


# Load and prepare the dataset
df = pd.read_csv("Mall_Customers.csv")
df = df.drop(["CustomerID", "Gender", "Age"], axis=1)
df.rename(columns={"Annual Income (k$)": "Income", "Spending Score (1-100)": "Spending"}, inplace=True)

# Determine optimal number of clusters using Elbow Method
wss = []  # Within-Cluster Sum of Squares
clusters_range = range(1, 2)
print(df['Income'].mean())
print(df['Spending'].mean())
for k in clusters_range: # for each k value
    model = KMeans(n_clusters=k, random_state=123) # create KMeans model    
    model.fit(df) 
    print(f'K={k}, Center={model.cluster_centers_}')
    #print(f'K={k}, WSS={model.inertia_}')
       # Cluster members
    # for cluster_num in range(k): # for each cluster
    #     members = df[model.labels_ == cluster_num]  # select points in this cluster
    #     print(f'\nCluster {cluster_num} members:')
    #     print(members)

