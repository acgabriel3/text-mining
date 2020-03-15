from sklearn.cluster import KMeans, AgglomerativeClustering


def kmeans(sparse_X_train, **kwargs):
    model = KMeans(**kwargs)
    return model.fit(sparse_X_train.toarray())


def agglomerative(sparse_X_train, **kwargs):
    model = AgglomerativeClustering(**kwargs)
    return model.fit(sparse_X_train.toarray())
