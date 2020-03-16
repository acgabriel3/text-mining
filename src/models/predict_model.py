from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import fcluster

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