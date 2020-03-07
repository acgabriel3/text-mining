# %%
%load_ext autoreload
%autoreload 2


# %%
import sys
import os
module_path = os.path.abspath(os.path.join('..', '..'))
if module_path not in sys.path:
    sys.path.append(module_path)


# %%
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
import sbrt_ibict_ml.sbrt_ibict_ml as sbrt


# %%
dossies = sbrt.data.get_dossies_df()
corpus = dossies.text

dossies.info()


# %%
vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(corpus)
X.shape


# %%
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

model = model.fit(X.toarray())
# plot the top three levels of the dendrogram
sbrt.plot_dendrogram(model, truncate_mode='level', p=3)

sbrt.plot_SVD_clusters(model, X, 5)


# %%
