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

###################### Load the data #######################
df = pd.read_csv("Mall_Customers.csv")
print(df.head())

###################### Initial Data Analysis #######################
# We might not need customer id and age for analysis remove those data frames
df = df.drop(["CustomerID","Gender","Age"], axis=1)
# Rename column names to simple names
df.rename({"Annual Income (k$)":"income", "Spending Score (1-100)":"Spending"}, axis=1, inplace=True)
print(df.head())

###################### Visualization of Data #######################
#plt.scatter(df["income"],df["Spending"]) # By looking at data we can figure out 5 clusters
#plt.show()

###################### Exploratory Data Analysis : Create the clusters #######################
# Why Cluster ?
    # 1. To group similar data points together
    # 2. Purpose of finding similar groups of customers is to target them with specific marketing strategies
kmean = KMeans(n_clusters=5, random_state=123455)
kmean.fit(df)
print("Clusters:")
print(kmean.n_clusters)

print("Cluster Centroind:")
print(kmean.cluster_centers_)

print("Cluster Centroind:")
print(kmean.labels_)

# ###################### Visualization of Cluster #######################
plt.scatter(df["income"][kmean.labels_==0],df["Spending"][kmean.labels_==0], color="brown", label="Cluster 1") # By looking at data we can figure out 5 clusters
plt.scatter(df["income"][kmean.labels_==1],df["Spending"][kmean.labels_==1], color="green", label="Cluster 2") 
plt.scatter(df["income"][kmean.labels_==2],df["Spending"][kmean.labels_==2], color="blue", label="Cluster 3") 
plt.scatter(df["income"][kmean.labels_==3],df["Spending"][kmean.labels_==3], color="orange", label="Cluster 4")
plt.scatter(df["income"][kmean.labels_==4],df["Spending"][kmean.labels_==4], color="black", label="Cluster 5")

## Print centroids
plt.scatter(kmean.cluster_centers_[:,0],kmean.cluster_centers_[:,1], color="red", label="Centroids")
# [:,0] is income and [:,1] is spending
# : means all rows and 0 means first column

plt.xlabel("Income")
plt.ylabel("Spending")
plt.legend()
plt.show()

# ###################### Find optimal number of cluster #######################
# Why to find optimal number of cluster?
# 1. To avoid overfitting
    # Overfitting is when the model learns the noise in the training data instead of the actual pattern.
# 2. To avoid underfitting
    # Underfitting is when the model is too simple to capture the underlying pattern in the data.
    # Underfitting can occur if the number of clusters is too low.
# 3. To avoid misclassification
    # Misclassification is when the model assigns a data point to the wrong cluster.
    # Misclassification can occur if the number of clusters is too high.    

wss=[] # Within the sum of square
clusters = np.arange(1,20) # Number of clusters

for cluster in clusters: # Iterate through the number of clusters
    kmeanObject = KMeans(n_clusters=cluster, random_state=123456) # Create the KMeans object
    kmeanObject.fit(df) # Fit the model to the data
    wss.append(kmeanObject.inertia_) # Append the inertia to the list

print(wss)
plt.scatter(clusters,wss)
#plt.plot(clusters,wss)

#plt.show()

