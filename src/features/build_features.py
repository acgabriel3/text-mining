from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


def get_tfidf_features(corpus):
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
    return vectorizer.fit_transform(corpus)
