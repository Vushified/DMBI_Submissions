#!/usr/bin/env python3
"""
Experiment 6: K-Means Clustering of EV Fleet Telemetry Dataset (Python).
Student: Vidushi Singh (Roll No. 53, D15A)
Course: Data Mining & Business Intelligence (DMBI Lab)
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score

np.random.seed(53)
sns.set_theme(style="whitegrid")

out_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(out_dir, "EV_Fleet_Preprocessed_Dataset.csv")
df = pd.read_csv(data_path)
print("=" * 60)
print(f"EXPERIMENT 6: K-MEANS CLUSTERING (Dataset Shape: {df.shape})")
print("=" * 60)

features = [
    'charging_duration_min',
    'energy_consumed_kwh',
    'initial_soc_pct',
    'final_soc_pct',
    'peak_power_kw',
    'avg_charging_c_rate',
    'battery_capacity_kwh',
    'ambient_temp_c',
    'session_cost_inr',
    'turnaround_urgency_score'
]

X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1. Elbow Method (Inertia/WCSS)
print("\nCalculating WCSS for K in range [2, 8]...")
k_range = list(range(2, 9))
inertia_list = []
for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=53)
    km.fit(X_scaled)
    inertia_list.append(km.inertia_)
    print(f"  k = {k} | WCSS = {km.inertia_:.2f}")

plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia_list, marker='o', color='#1565C0', lw=2.2, markersize=7)
plt.axvline(x=4, color='#D32F2F', linestyle='--', label='Optimal Elbow k = 4')
plt.title("Elbow Method for Optimal Clusters (WCSS vs K)", fontweight='bold')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
plt.legend()
plt.tight_layout()
elbow_path = os.path.join(out_dir, "elbow_curve.png")
plt.savefig(elbow_path, dpi=180)
plt.close()
print(f"Saved: {elbow_path}")

# 2. Optimal K-Means Clustering (k = 4)
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', n_init=10, random_state=53)
cluster_labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = cluster_labels

# Validation Metrics
# Sample 5000 points for silhouette computation speed
sample_idx = np.random.choice(len(X_scaled), size=5000, replace=False)
sil_score = silhouette_score(X_scaled[sample_idx], cluster_labels[sample_idx])
db_score = davies_bouldin_score(X_scaled, cluster_labels)
print(f"\n--- Cluster Validation Metrics (k=4) ---")
print(f"Silhouette Score (Cohesion & Separation): {sil_score:.4f}")
print(f"Davies-Bouldin Index (Lower is Better):   {db_score:.4f}")

# 3. Cluster Sizes Bar Chart
plt.figure(figsize=(7, 4.5))
cluster_counts = df['Cluster'].value_counts().sort_index()
cluster_names = [
    'Cluster 0: Fleet Express Fast DC',
    'Cluster 1: Urban Commuter Top-Up',
    'Cluster 2: Overnight Slow AC Depot',
    'Cluster 3: Ultra-Fast Highway Corridor'
]
bars = plt.bar(range(4), cluster_counts.values, color=['#1976D2', '#388E3C', '#F57C00', '#7B1FA2'], width=0.6)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 150, f"{yval:,} ({yval/len(df)*100:.1f}%)", ha='center', va='bottom', fontsize=9)
plt.xticks(range(4), ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3'])
plt.title("EV Charging Cluster Distribution (N = 20,000)", fontweight='bold')
plt.ylabel("Number of Sessions")
plt.tight_layout()
sizes_path = os.path.join(out_dir, "cluster_sizes.png")
plt.savefig(sizes_path, dpi=180)
plt.close()
print(f"Saved: {sizes_path}")

# 4. 2D PCA Cluster Scatter
pca = PCA(n_components=2, random_state=53)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(9, 6.5))
palette = ['#1976D2', '#388E3C', '#F57C00', '#7B1FA2']
for c in range(optimal_k):
    plt.scatter(X_pca[cluster_labels == c, 0], X_pca[cluster_labels == c, 1],
                label=cluster_names[c], alpha=0.5, s=20, color=palette[c])
# Plot Centroids in PCA space
centroids_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], s=180, c='black', marker='X', label='Centroids')
plt.title(f"2D PCA Projection of EV Charging Clusters (k=4, Explained Var: {sum(pca.explained_variance_ratio_)*100:.1f}%)", fontweight='bold')
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
scatter_path = os.path.join(out_dir, "cluster_scatter.png")
plt.savefig(scatter_path, dpi=180)
plt.close()
print(f"Saved: {scatter_path}")

# 5. Cluster Profiles
print("\n--- Cluster Mean Centroid Profiles (Original Scale) ---")
profile = df.groupby('Cluster')[features].mean().T
profile.columns = [f"Cluster {i}" for i in range(4)]
print(profile)

out_profile_csv = os.path.join(out_dir, "kmeans_cluster_profiles.csv")
profile.to_csv(out_profile_csv)
print(f"\nCluster profiles saved to: {out_profile_csv}")

