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
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
import sbrt_ibict_ml.sbrt_ibict_ml as sbrt
import matplotlib.pyplot as plt
import numpy as np


# %%
dossies = sbrt.get_dossies_df(size=50)
corpus = dossies.text
dossies.info()


# %%
metadados = sbrt.get_dossies_metadados_df(dossies.file)
metadados.info()


# %%
vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(corpus)
X.shape


# %%
agglomerative = AgglomerativeClustering(distance_threshold=0, n_clusters=None, linkage='complete')
agglomerative = agglomerative.fit(X.toarray())
agglomerative


# %%
sbrt.plot_dendrogram(agglomerative)
dend_labels = agglomerative.labels_


# %%
agglomerative.distance_threshold = None
sbrt.plot_SVD_clusters(agglomerative, X, 10)
aggl_labels = agglomerative.labels_


# %%
# isso está correto mesmo? apesar da inercia diminuir, parece n convergir
kmeans = KMeans()
sbrt.plot_KMeans_inertia(kmeans, X, 20)


# %%
sbrt.plot_SVD_clusters(kmeans, X, 10)
kmeans_labels = kmeans.labels_


# %%
# dendrogram vs agglomerative
np.sum(dend_labels != aggl_labels)


# %%
# dendrogram vs kmeans
np.sum(dend_labels != kmeans_labels)


# %%
# agglomerative vs kmeans
np.sum(aggl_labels != kmeans_labels)


# %%
