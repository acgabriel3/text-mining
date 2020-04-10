from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import fcluster
import numpy as np


def kmeans(model, sparse_X_test):
    """
    prediz as labels utilizando o algoritmo KMeans

    Parameters
    ----------
    model : `KMeans`
        classe do sklearn.cluster

    sparse_X_test: X
        matriz esparsa

    Returns
    -------
    labels:
        index do cluster no qual cada dado pertence
    """
    return model.predict(sparse_X_test.toarray())


def linkage_matrix(model):
    """
    gera a matriz Z utilizando o Agglomerative Clustering

    Parameters
    ----------
    model : `AgglomerativeClustering`
        classe do sklearn.agglomerative_clustering

    Returns
    -------
    linkage matrix:
        representação da matriz Z
    """
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

    return np.column_stack([model.children_, model.distances_,
                            counts]).astype(float)


def Z_labels(Z, **kwargs):
    """
    retorna os indexes dos clusters baseado na matriz Z

    Parameters
    ----------
    Z : `Z`
        linkage matrix

    **kwargs:
        lista de parametros para serem passados para a função
        fcluster do scipy

    Returns
    -------
    labels:
        index do cluster no qual cada dado pertence 
    """
    return fcluster(Z, **kwargs)
