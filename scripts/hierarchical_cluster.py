# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import append_sbrt_module


# %%
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering, KMeans
from nltk.corpus import stopwords
import pandas as pd, seaborn as sns, matplotlib as mpl
import sbrt_ibict_ml.sbrt_ibict_ml as sbrt
import matplotlib.pyplot as plt
import numpy as np


#%%
# mpl.use('webAgg')  # abre um navegador pra visualizar o gráfico gerado


# %%
dossies = sbrt.get_dossies_df(size=5)
corpus = dossies.text
print(corpus.head())


# %%
vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(corpus)
print(X.shape)


# %%
den = dendrogram(linkage(X.toarray(), method='ward'))
plt.figure(0)
plt.show()


# %%
metadados = sbrt.get_dossies_metadados_df(dossies.file, ['titulo', 'palavras_chave', 'categoria'])
print(metadados.head())


# %%
dendrogram_model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, linkage='ward').fit(X.toarray())
plt.figure(1)
sbrt.plot_dendrogram(dendrogram_model)


# %%
# para ir checando ainda manual as categorias dos clusters
[c for c in metadados.loc[[0,1]].categoria]


# %%
# plota o gráfico do dendrograma pode-se dizer, mas pelo que parece cada ponto tem uma label
svd = TruncatedSVD()
scatter_plot_points = svd.fit_transform(X.toarray())

xs = [o[0] for o in scatter_plot_points]
ys = [o[1] for o in scatter_plot_points]

plt.figure(2)
plt.scatter(x=xs, y=ys, c=dendrogram_model.labels_)
plt.show()


# %%
plt.figure(3)
sbrt.plot_N_clusters(AgglomerativeClustering(linkage='complete'), X, 3)


# %%
plt.figure(4)
sbrt.plot_N_clusters(KMeans(), X, 3)


# %%


