import nltk as nltk
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from os import listdir
from os.path import isfile, join


path = "D:/curso_ciencia_da_computacao/pesquisa com Prof.Ricardo/text-mining/dados/sbrt_txts/dossies"
files = [ f for f in listdir(path) if isfile(join(path,f)) ]

dossies = pd.DataFrame(data = None, columns = ['dossie', 'texto'])

for file in files:
    with open(file) as f:
        global text
        text = f.readlines()
        aux = pd.DataFrame(data = [[file, text]], columns = ['dossie', 'texto'])
        dossies = pd.DataFrame.append(dossies, aux, ignore_index = True) 
        

def retiraPontuacao(texto):
    semPontuacao = "".join([c for c in texto if c not in string.punctuation])
    return semPontuacao


dossies['texto'] = dossies['texto'].apply(retiraPontuacao)

dossies['texto'] = dossies['texto'].apply(lambda x : word_tokenize(x.lower(), language = 'portuguese'))

def remove_palavras_fracas(texto):
    palavras = [w for w in texto if w not in stopwords.words('portuguese')]
    return palavras

dossies['texto'][0] =  remove_palavras_fracas(dossies['texto'][0])

# O processo para retirar stopwords se mostrou extremamente lento ateh o momento
#dossies['texto'][0].apply(lambda x : remove_palavras_fracas(x))




















































