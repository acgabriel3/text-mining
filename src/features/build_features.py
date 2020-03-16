from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


def get_tfidf_features(corpus):
    """
    retorna um array com a medida tf-idf para cada palavra contida no corpus

    Parameters
    ----------
    corpus : `list` of `str`
        representando o conjunto de textos que serão utilizados nos modelos
        de aprendizagem de máquina

    Returns
    -------
    X:
        Matriz esparsa utilizada de entrada nos algoritmos de Machine Learning
    """
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
    return vectorizer.fit_transform(corpus)
