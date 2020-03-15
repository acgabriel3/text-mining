from sklearn.cluster import KMeans, AgglomerativeClustering


def kmeans(model, sparse_X_test):
    return model.predict(sparse_X_test.toarray())
