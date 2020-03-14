# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import matplotlib.pyplot as plt
import sbrt_ibict_ml.sbrt_ibict_ml as sbrt
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering, KMeans
import os
import sys
from IPython import get_ipython

# %%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# %%
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


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
agglomerative = AgglomerativeClustering(
    distance_threshold=0, n_clusters=None, linkage='complete')
agglomerative = agglomerative.fit(X.toarray())
agglomerative


# %%
sbrt.plot_dendrogram(agglomerative)
dend_labels = agglomerative.labels_


# %%
agglomerative.distance_threshold = None
sbrt.plot_N_clusters(agglomerative, X, 10)
aggl_labels = agglomerative.labels_


# %%
# isso está correto mesmo? apesar da inercia diminuir, parece n convergir
kmeans = KMeans()
sbrt.plot_KMeans_inertia(kmeans, X, 20)


# %%
sbrt.plot_N_clusters(kmeans, X, 10)
kmeans_labels = kmeans.labels_
