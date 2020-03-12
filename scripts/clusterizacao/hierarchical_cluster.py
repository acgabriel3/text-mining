# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# %%
import sys
import os
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


# %%
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
from nltk.corpus import stopwords
import pandas as pd, seaborn as sns, matplotlib as mpl
import sbrt_ibict_ml.sbrt_ibict_ml as sbrt
import matplotlib.pyplot as plt
import numpy as np


# %%
# mpl.style.use('seaborn')


# %%
dossies = sbrt.get_dossies_df()
corpus = dossies.text
dossies.info()


# %%
vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(corpus)
X.shape


# %%
n_clusters = 464
Z = linkage(pd.DataFrame(data=X.toarray()), 'complete')
dossies['cluster_label'] = fcluster(Z, n_clusters, criterion='maxclust')
Z


# %%
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z, truncate_mode='level', p=3, leaf_rotation=0)
plt.autoscale()
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()


# %%
svd = TruncatedSVD()
scatter_plot_points = svd.fit_transform(X.toarray())

dossies['xs'] = [o[0] for o in scatter_plot_points]
dossies['ys'] = [o[1] for o in scatter_plot_points]

plt.scatter(x=xs, y=ys, c=dossies.cluster_label)


# %%
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
model.fit(X.toarray())
sbrt.plot_dendrogram(model, truncate_mode='level', p=3, leaf_rotation=90)
plt.show()


# %%
scatter_plot_points = svd.fit_transform(X.toarray())

xs = [o[0] for o in scatter_plot_points]
ys = [o[1] for o in scatter_plot_points]
fig, ax = plt.subplots()

# ax.set_title(f'Clustering with {k} clusters')
plt.scatter(x=xs, y=ys, c=model.labels_)
# ax.scatter(xs, ys, c=model.labels_, alpha=.7)


# %%


