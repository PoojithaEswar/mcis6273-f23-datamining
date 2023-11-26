
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('country_violations_year_month_2014-2023.csv')

# Map month names to numerical values
month_mapping = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

df['MONTH'] = df['MONTH'].map(month_mapping)

# Select relevant columns for clustering
X = df[['YEAR', 'MONTH', 'VIOLATION_COUNT']]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-means clustering with K = 5
kmeans_5 = KMeans(n_clusters=5, random_state=42)
df['Cluster_5'] = kmeans_5.fit_predict(X_scaled)

# Perform K-means clustering with K = 10
kmeans_10 = KMeans(n_clusters=10, random_state=42)
df['Cluster_10'] = kmeans_10.fit_predict(X_scaled)

# Perform K-means clustering with K = 12
kmeans_12 = KMeans(n_clusters=12, random_state=42)
df['Cluster_12'] = kmeans_12.fit_predict(X_scaled)

# Print centroids for each cluster
print("Centroids for K = 5:")
print(scaler.inverse_transform(kmeans_5.cluster_centers_))
print("\nCentroids for K = 10:")
print(scaler.inverse_transform(kmeans_10.cluster_centers_))
print("\nCentroids for K = 12:")
print(scaler.inverse_transform(kmeans_12.cluster_centers_))

# Describe each cluster for K = 5
for cluster in range(5):
    cluster_data = df[df['Cluster_5'] == cluster]
    print(f"\nCluster {cluster} (K = 5):")
    print(cluster_data.describe())

# Describe each cluster for K = 10
for cluster in range(10):
    cluster_data = df[df['Cluster_10'] == cluster]
    print(f"\nCluster {cluster} (K = 10):")
    print(cluster_data.describe())

# Describe each cluster for K = 12
for cluster in range(12):
    cluster_data = df[df['Cluster_12'] == cluster]
    print(f"\nCluster {cluster} (K = 12):")
    print(cluster_data.describe())




# AElbow Analysis to find optimal cluster size

max_clusters = 15
css = []  # within-cluster sum of squares

for k in range(1, max_clusters):
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10, random_state=0)
    kmeans.fit(X_scaled)
    css.append(kmeans.inertia_)

# Plotting the Elbow Graph
plt.figure(figsize=(8, 6))
plt.plot(range(1, max_clusters), css, marker='o', linestyle='-', color='b')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Within-Cluster Sum of Squares (CSS)')
plt.show()

# Determine the optimal K
optimal_k = int(input("Enter the optimal number of clusters (K) from the elbow plot: "))

# Re-run clustering with optimal K
kmeans_optimal = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=200, n_init=10, random_state=0)
df['Optimal_Cluster'] = kmeans_optimal.fit_predict(X_scaled)

# Print centroids for optimal clustering
print(f"Centroids for Optimal K ({optimal_k}):")
print(scaler.inverse_transform(kmeans_optimal.cluster_centers_))

# Describe each cluster for optimal K
for cluster in range(optimal_k):
    cluster_data = df[df['Optimal_Cluster'] == cluster]
    print(f"\nCluster {cluster} (Optimal K):")
    print(cluster_data.describe())
