from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords


def get_tfidf_features(corpus, n_features=None):
    """
    retorna um array com a medida tf-idf para cada palavra contida no corpus

    Parameters
    ----------
    corpus : `list` of `str`
        representando o conjunto de textos que serão utilizados nos modelos
        de aprendizagem de máquina

    n_features: `int`
        quantidade maxima de features a serem extraidas    
    Returns
    -------
    (X, feature_names):
        (Matriz esparsa utilizada de entrada nos algoritmos de Machine Learning, feature_names)
    """
    vectorizer = TfidfVectorizer(
        max_features=n_features, stop_words=stopwords.words('portuguese')
    )
    return (vectorizer.fit_transform(corpus), vectorizer.get_feature_names())


def get_tf_features(corpus, n_features=None):
    """
    retorna um array com a medida tf-idf para cada palavra contida no corpus

    Parameters
    ----------
    corpus : `list` of `str`
        representando o conjunto de textos que serão utilizados nos modelos
        de aprendizagem de máquina

    n_features: `int`
        quantidade maxima de features a serem extraidas    
    Returns
    -------
    (X, feature_names):
        (Matriz esparsa utilizada de entrada nos algoritmos de Machine Learning, feature_names)
    """
    vectorizer = CountVectorizer(
        max_features=n_features, stop_words=stopwords.words('portuguese')
    )
    vectorizer._validate_vocabulary()
    return (vectorizer.fit_transform(corpus), vectorizer.get_feature_names())
