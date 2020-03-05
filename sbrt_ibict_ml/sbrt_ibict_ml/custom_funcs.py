# %%
import nltk
import string
import re
import PyPDF2
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt


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
def plot_SVD_clusters(model, X):
    pca = TruncatedSVD()
    for k in range(2, 20):
        model.n_clusters = k
        model.fit(X.toarray())
        scatter_plot_points = pca.fit_transform(X.toarray())

        xs = [o[0] for o in scatter_plot_points]
        ys = [o[1] for o in scatter_plot_points]
        fig, ax = plt.subplots()

        ax.set_title(f'Clustering with {k} clusters')
        ax.scatter(xs, ys, c=model.labels_, alpha=.7)
