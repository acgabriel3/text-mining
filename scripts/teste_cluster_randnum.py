# Perform the necessary imports
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mpl.use('webAgg')  # abre um navegador pra visualizar o gráfico gerado


def visualize_cluster_inertia(samples):
    ks = range(1, 15)
    inertias = []
    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters=k)

        # Fit model to samples
        model.fit(samples)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    # Plot ks vs inertias
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    # plt.show()


np.random.seed(42)
N_SAMPLES = 300
N_LABELS = 6
samples = np.array(np.random.random((N_SAMPLES, 3)) * (np.random.random() * 100))
samples_labels = np.array(np.random.choice(N_LABELS, N_SAMPLES))

# visualize_cluster_inertia(samples)

# Create scaler: scaler
scaler = StandardScaler()
# Create KMeans instance: kmeans
kmeans = KMeans(n_clusters=N_LABELS)
# Create pipeline: pipeline
pipeline = make_pipeline(scaler, kmeans)

# Fit the pipeline to samples
pipeline.fit(samples)
# Calculate the cluster labels: labels
labels = pipeline.predict(samples)

# Create a DataFrame with labels and species as columns: df
df = pd.DataFrame({'labels': labels, 'real_labels': samples_labels})
# Create crosstab: ct
ct = pd.crosstab(df.labels, df.real_labels)

# Display ct
print(ct)

# plot graphic with clusters
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('feature 1')
ax.set_ylabel('feature 2')
ax.set_zlabel('feature 3')

x = samples[:, 0]
y = samples[:, 1]
z = samples[:, 2]

ax.scatter(x, y, z, c=labels, marker='o')
plt.show()
