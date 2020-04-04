from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage
from sklearn.decomposition import LatentDirichletAllocation, NMF


def kmeans(sparse_X_train, **kwargs) -> KMeans:
    """
    treina utilizando o algoritmo KMeans

    Parameters
    ----------
    sparse_X_train: `X`
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
    sparse_X_train: `X`
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


def linkage_matrix(sparse_X_train, **kwargs):
    """
    faz clusterização hierarquica.

    Parameters
    ----------
    sparse_X_train: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para a função
        linkage do scipy

    Returns
    -------
    linkage_matrix: `Z` 
    """
    return linkage(sparse_X_train.toarray(), **kwargs)


def lda(sparse_X_train, n_topics, **kwargs):
    """
    treina utilizando o algoritmo LDA

    Parameters
    ----------
    sparse_X_train: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para o contrutor da classe
        LDA

    Returns
    -------
    LatentDirichletAllocation:
        modelo treinado 
    """
    return LatentDirichletAllocation(n_components=n_topics,
                                     max_iter=5,
                                     learning_method='online',
                                     learning_offset=50.0,
                                     **kwargs
                                     ).fit(sparse_X_train)


def nmf(sparse_X_train, n_topics, **kwargs):
    """
    treina utilizando o algoritmo NMF

    Parameters
    ----------
    sparse_X_train: `X`
        matriz esparsa

    **kwargs:
        lista de parametros para serem passados para o contrutor da classe
        NMF

    Returns
    -------
    NMF:
        modelo treinado 
    """
    return NMF(
        n_components=n_topics,
        alpha=.1,
        l1_ratio=.5,
        init='nndsvd',
        **kwargs
    ).fit(sparse_X_train)
