import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import TruncatedSVD
from ..models import train_model, predict_model
from adjustText import adjust_text


def show():
    """
    deve ser chamado apenas uma vez ao final do programa
    """
    plt.show()


def plot_dendrogram_Agglomerative(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    plt.figure()
    plt.title('Hierarchical Clustering Dendrogram with agglomerative')
    # plot the top three levels of the dendrogram
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    dendrogram(linkage_matrix, **kwargs)


def plot_dendrogram(Z, **kwargs):
    plt.figure()
    plt.title('Hierarchical Clustering Dendrogram with linkage')
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    dendrogram(Z, **kwargs)


def plot_N_clusters_KMeans(sparse_X_test, max_range=10, plot_index_labels=False):
    for k in range(2, max_range):
        plot_KMeans(sparse_X_test, plot_index_labels)


def plot_KMeans(sparse_X_test, plot_index_labels=False):
    kmeans = train_model.kmeans(sparse_X_test)
    labels = predict_model.kmeans(kmeans, sparse_X_test)
    plot_SVD(kmeans.n_clusters, sparse_X_test, labels, plot_index_labels)


def plot_N_clusters_Agglomerative(sparse_X_test, max_range=10, plot_index_labels=False):
    for k in range(2, max_range):
        plot_SVD(
            k,
            sparse_X_test,
            train_model.agglomerative(sparse_X_test, n_clusters=k).labels_,
            plot_index_labels
        )


def plot_SVD(n_cluster, sparse_X_test, labels, plot_index_labels):
    svd = TruncatedSVD()
    scatter_plot_points = svd.fit_transform(sparse_X_test.toarray())

    xs = [o[0] for o in scatter_plot_points]
    ys = [o[1] for o in scatter_plot_points]
    fig, ax = plt.subplots()

    ax.set_title(f'Clustering with {n_cluster} clusters')
    ax.scatter(xs, ys, c=labels, alpha=.7)

    if plot_index_labels:
        texts = [
            plt.text(xs[i], ys[i], f'{i, labels[i]}') for i in range(len(xs))
        ]
        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))


def plot_KMeans_inertia(sparse_X_test, max_range=14):
    ks = range(2, max_range + 1)
    inertias = []
    for k in ks:
        kmeans = train_model.kmeans(sparse_X_test, n_clusters=k)
        predict_model.kmeans(kmeans)
        # Append the inertia to the list of inertias
        inertias.append(kmeans.inertia_)

    # Plot ks vs inertias
    plt.figure()
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
