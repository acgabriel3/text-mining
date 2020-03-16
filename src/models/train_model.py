from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage


def kmeans(sparse_X_train, **kwargs) -> KMeans:
    """
    treina utilizando o algoritmo KMeans

    Parameters
    ----------
    sparse_X_test: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para o contrutor da classe
        KMeans

    Returns
    -------
    KMeans:
        modelo treinado 
    """
    model = KMeans(**kwargs)
    return model.fit(sparse_X_train.toarray())


def agglomerative(sparse_X_train, **kwargs) -> AgglomerativeClustering:
    """
    treina utilizando o algoritmo AgglomerativeClustering

    Parameters
    ----------
    sparse_X_test: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para o contrutor da classe
        AgglomerativeClustering

    Returns
    -------
    AgglomerativeClustering:
        modelo treinado 
    """
    model = AgglomerativeClustering(**kwargs)
    return model.fit(sparse_X_train.toarray())


def linkage_matrix(sparse_X_test, **kwargs):
    """
    faz clusterização hierarquica.

    Parameters
    ----------
    sparse_X_test: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para a função
        linkage do scipy

    Returns
    -------
    linkage_matrix: `Z` 
    """
    return linkage(sparse_X_test.toarray(), **kwargs)
