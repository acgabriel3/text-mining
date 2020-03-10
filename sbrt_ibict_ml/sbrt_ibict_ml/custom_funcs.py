# %%
import nltk
import string
import re
import PyPDF2
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from adjustText import adjust_text


# %%
# se o nltk der problema para rodar descomente essa parte
# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('rslp')


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
def basic_pre_processing(text):
    stop_words = nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()

    # remove pontuação da forma mais eficiente possivel
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    text = re.sub(r'serviço brasileiro de respostas técnicas', '', text)
    text = re.sub(r'dossiê técnico', '', text)
    text = re.sub(r'd o s si ê t é c n i c o', '', text)

    tokens = nltk.word_tokenize(text, language='portuguese')

    no_stop_words_txt = " ".join(
        [word for word in tokens if word not in [stop_words, 'copyright', '©', 'sbrt', 'httpwwwsbrtibictbr', "˙˘˙"]])

    return "".join([stemmer.stem(word) for word in no_stop_words_txt])


# %%
# necessária se fosse ler os PDF's utilizando o PyPDF2
def get_pdf_content(file):
    pdf = PyPDF2.PdfFileReader(file)
    return " ".join([basic_pre_processing(pdf.getPage(i).extractText())
                     for i in range(1, pdf.numPages)])


# %%
def plot_SVD_clusters(model, X, max_range=20, plot_index_labels=False):
    svd = TruncatedSVD()

    for k in range(2, max_range):
        model.n_clusters = k
        model.fit(X.toarray())
        scatter_plot_points = svd.fit_transform(X.toarray())

        xs = [o[0] for o in scatter_plot_points]
        ys = [o[1] for o in scatter_plot_points]
        fig, ax = plt.subplots()

        ax.set_title(f'Clustering with {k} clusters')
        ax.scatter(xs, ys, c=model.labels_, alpha=.7)

        if plot_index_labels:
            texts = [
                plt.text(xs[i], ys[i], f'{i, model.labels_[i]}') for i in range(len(xs))]
            adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))


# %%
# Create linkage matrix and then plot the dendrogram
def plot_dendrogram(model, **kwargs):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.show()


# %%
def plot_KMeans_inertia(model, X, max_range=15):
    ks = range(2, max_range)
    inertias = []
    for k in ks:
        model.n_clusters = k
        model.fit(X)
        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    # Plot ks vs inertias
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()

