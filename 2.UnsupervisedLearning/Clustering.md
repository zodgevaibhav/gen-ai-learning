# 🧪 Exploratory Data Analysis: Creating Clusters

Clustering is a powerful **unsupervised learning** technique used in data analysis to group similar data points together. It helps identify **homogeneous subgroups** in a dataset, enabling better understanding and decision-making.

---

## 📌 What is Clustering?

- Clustering is the process of **grouping and subgrouping** data points based on similarity.
- It is used to **uncover hidden patterns** in data.
- Often applied in:
  - **Customer Segmentation**: Upper class / Middle class / Lower class | Spending: High / Medium / Low
  - **Biology**: Grouping similar species
  - **Image Processing**: Segmenting similar pixels
  - **Document Analysis**: Grouping related documents

---

## ❗ Common Challenges in Clustering

1. How to determine the **number of clusters**?
2. What is the **optimal number of clusters**?
3. No labeled data → **No ground truth** for validation
4. Can be **computationally expensive**
5. May not always be **accurate or reliable**
6. **Hard to interpret** cluster meaning
7. Sometimes **difficult to visualize** especially in high dimensions

---

## 🔍 EDA Process for Clustering

1. Load the data
2. Visualize the data
3. Preprocess the data (cleaning, scaling, etc.)
4. Create the clusters
5. Visualize the clusters
6. Determine the **optimal number of clusters**
7. Use methods like:
   - **Elbow Method**
   - **Silhouette Score**
   - **Gap Statistic**
8. Visualize results of each method to interpret clusters

---

## 🔄 Example: EDA + Clustering Workflow

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Step 1: Load data
df = pd.read_csv("data.csv")

# Step 2: Preprocess
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Step 3: Elbow method to find optimal k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)

# Step 4: Plot
plt.plot(range(1, 11), sse)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("SSE (Inertia)")
plt.title("Elbow Method")
plt.show()
```

## 🔣 Types of Clustering

### 1. 📍 Centroid-Based Clustering

Relies on **central points (centroids)** to form clusters.  
**KMeans** is the most common example.

#### 🔁 KMeans Algorithm Steps:

- Choose number of clusters (`k`)
- Initialize centroids
- Assign each data point to the nearest centroid
- Recalculate centroids as the mean of assigned points
- Repeat until convergence (no change in centroids)

#### ✅ Example Use Cases:

- Customer segmentation  
- Product categorization

---

### 2. 🔘 Density-Based Clustering

Clusters are formed where **data points are densely packed**.  
**DBSCAN** is a popular algorithm.

#### 🔁 DBSCAN Algorithm Steps:

- Choose `eps` (radius) and `minPts` (minimum neighbors)
- For each point, find neighbors within `eps`
- If neighbors ≥ `minPts`, mark as **core point**
- Expand cluster by connecting neighboring core points
- Identify **noise/outliers** as points not in any cluster

#### ✅ Example Use Cases:

- Anomaly detection  
- Clustering spatial data

---

### 🔬 Visualizing Silhouette Score (DBSCAN)

```python
from sklearn.metrics import silhouette_score

# Assume labels are obtained from DBSCAN
score = silhouette_score(scaled_data, labels)
print("Silhouette Score:", score)
```

## 📊 How to Evaluate Clustering

### 📌 Elbow Method

- Plot the **inertia (SSE)** against different values of `k`
- Look for the **“elbow” point** where the curve bends — this is often the optimal number of clusters

### 📌 Silhouette Score

- Measures how similar a data point is to its **own cluster** compared to **other clusters**
- Score ranges from **-1 to 1**
    - Closer to **1** indicates well-separated clusters
    - **0** indicates overlapping clusters
    - **Negative** values indicate potential misclassification

### 📌 Gap Statistic

- Compares the **total within-cluster variation** for different values of `k` with their expected values under a **null reference distribution**
- The optimal `k` is where the **gap between the two is largest**
