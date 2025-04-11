# Unsupervised Learning

Unsupervised learning is a type of machine learning where the model is trained on **unlabeled data**—meaning there are no predefined outputs or target values. The goal is for the algorithm to find hidden patterns, structures, or relationships in the data without human supervision.

## Key Features of Unsupervised Learning

- **No Labeled Data**: Unlike supervised learning, the algorithm does not receive input-output pairs.
- **Finds Patterns and Structures**: Detects similarities, clusters, or anomalies in the data.
- **Self-Organizing**: Groups data based on its inherent structure.

## Common Unsupervised Learning Techniques

![Mindmap of Unsupervised Learning Techniques](./images/MindMap.png)

### 1. Clustering
- **Description**: Grouping similar data points together.
- **Example Algorithms**: K-Means, DBSCAN, Hierarchical Clustering.
    #### K-Means Algorithm
    - **Description**: K-Means is a clustering algorithm that partitions data into `k` clusters, where each data point belongs to the cluster with the nearest mean.
    - **Steps**:
        1. Choose the number of clusters (K)
            The user specifies the number of clusters KK.
            A good value for KK can be chosen using methods like the Elbow Method or Silhouette Score.
        2. Initialize KK cluster centroids
            Select KK initial cluster centers randomly from the dataset or use the K-Means++ method for better initialization.
        3. Assign each data point to the nearest cluster centroid
            Compute the Euclidean distance (or another distance metric) between each data point and all centroids.
            Assign each data point to the closest centroid.
        4. Compute new cluster centroids
            For each cluster, compute the mean (average) of all the points assigned to it.
            Update the cluster centroids with these new values.
        5. Repeat steps 3 and 4 until convergence
            Continue reassigning points and updating centroids until:
                Centroids do not change significantly (or)
                A maximum number of iterations is reached.
        6. Output final clusters
            The algorithm returns KK clusters with their centroids.
            Data points are labeled according to their cluster.

        #### Example of K-Means in Action ####
        Imagine you have customer data and want to segment them into three groups (K=3K=3):
        1. The algorithm initializes 3 random centroids.
        2. Each customer is assigned to the closest centroid.
        3. The centroids are updated based on the average location of customers in each cluster.
        4. This process repeats until the clusters stabilize.

    - **Advantages**:
        - Simple and easy to implement.
        - Works well with large datasets.
    - **Disadvantages**:
        - Requires the number of clusters (`k`) to be specified beforehand.
        - Sensitive to the initial placement of centroids.
        - Struggles with non-spherical clusters or clusters of varying sizes.
    - **Use Case**: Segmenting customers based on purchasing behavior.

    - **Use Case**: Customer segmentation in marketing.

### 2. Dimensionality Reduction
- **Description**: Reducing the number of features while preserving important information.
- **Example Algorithms**: PCA (Principal Component Analysis), t-SNE, Autoencoders.
- **Use Case**: Data visualization, feature extraction in large datasets.

### 3. Anomaly Detection
- **Description**: Identifying rare or unusual data points.
- **Example Algorithms**: Isolation Forest, One-Class SVM.
- **Use Case**: Fraud detection in banking.

### 4. Association Rule Learning
- **Description**: Discovering relationships between variables.
- **Example Algorithms**: Apriori, FP-Growth.
- **Use Case**: Market Basket Analysis (e.g., "People who buy milk also buy bread").

## Real-World Applications

- Recommender systems (e.g., Netflix, Amazon).
- Image segmentation (e.g., facial recognition).
- Customer behavior analysis.
- Anomaly detection in cybersecurity.