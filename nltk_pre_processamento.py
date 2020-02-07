import nltk as nltk
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import RSLPStemmer
from os import listdir
from os.path import isfile, join
from collections import Counter


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

palavrasFracas = stopwords.words('portuguese')
palavras_fracas_dict = Counter(palavrasFracas)

def remove_palavras_fracas(texto):
    palavras = ''.join([word for word in str(texto).split() if word not in palavras_fracas_dict])
    
    #O metodo abaixo eh muito lento
    #[w for w in texto if w not in stopwords.words('portuguese')]
    return palavras

dossies['texto'] =  dossies['texto'].apply(lambda x : remove_palavras_fracas(x))

dossiesLem = dossies

#Exemplo para lematizacao
lematizador = WordNetLemmatizer()


#Sem suporte para o portugues pelo visto
def lematizaPalavras(texto):
    lemTexto = [lematizador.lemmatize(i) for i in texto]
    return lemTexto

dossiesLem['texto'] = dossiesLem['texto'].apply(lambda x : lematizaPalavras(x))


#Exemplo para stemmer

stemmer = RSLPStemmer() 

def stemmerPalavras(texto):
    stemTexto = "".join([stemmer.stem(i) for i in texto])
    return stemTexto

dossiesStem = dossies

dossiesStem['texto'] = dossiesStem['texto'].apply(lambda x : stemmerPalavras(x))























































