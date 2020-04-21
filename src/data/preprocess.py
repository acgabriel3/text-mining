import re
import nltk
import string
from unicodedata import normalize
import nltk


def pre_process(text):
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    table = str.maketrans('', '', string.punctuation)
    t = normalize('NFD', text).encode('ascii', 'ignore')
    t = t.decode('UTF-8')
    t = re.sub('Copyright  Servico Brasileiro de Respostas Tecnicas - SBRT - http://www.sbrt.ibict.br', '', t)
    t = re.sub(r'^https?:\/\/.*[\s]*', '', t)
    t = re.sub(r'\S*@\S*\s?', '', t)
    t = t.split()
    t = [word.lower() for word in t]
    t = [word.translate(table) for word in t]
    t = [re_print.sub('', w) for w in t]
    t = [word for word in t if word.isalpha()]
    t = [
        word for word in t
        if word not in nltk.corpus.stopwords.words('portuguese')
    ]
    return ' '.join(t)
