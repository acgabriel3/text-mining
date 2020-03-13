# %%
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from adjustText import adjust_text
from sklearn.cluster import KMeans


# %%
def create_vocabulary(words):
    d = {}
    counter = 1

    def update_dict(d, w, c):
        d[w] = counter
        return d

    def f(w, counter, d=d): return d if w in d else update_dict(d, w, counter)

    for w in words:
        f(w, counter)
        counter = counter + 1

    return d


# %%
def plot_SVD_clusters(model, X_test, max_range=19, plot_index_labels=False):
    svd = TruncatedSVD()
    inner_model = model
    for k in range(2, max_range + 1):
        inner_model.n_clusters = k
        inner_model.fit(X_test.toarray())
        scatter_plot_points = svd.fit_transform(X_test.toarray())

        xs = [o[0] for o in scatter_plot_points]
        ys = [o[1] for o in scatter_plot_points]
        fig, ax = plt.subplots()

        ax.set_title(f'Clustering with {k} clusters')
        ax.scatter(xs, ys, c=inner_model.labels_, alpha=.7)

        if plot_index_labels:
            texts = [
                plt.text(xs[i], ys[i], f'{i, inner_model.labels_[i]}') for i in range(len(xs))
            ]
            adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))


# %%
def plot_dendrogram(model, **kwargs):
    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack(
        [children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.show()


# %%
# plota n graficos, cada um com n clusters sendo
def plot_KMeans_inertia(X_test, max_range=14):
    ks = range(2, max_range + 1)
    inertias = []
    for k in ks:
        kmeans = KMeans(n_clusters=k)
        kmeans.predict(X_test)
        # Append the inertia to the list of inertias
        inertias.append(kmeans.inertia_)

    # Plot ks vs inertias
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()

# %%
