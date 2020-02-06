import nltk as nltk
import pandas as pd
import string
from bs4 import BeatifulSoup
from nltk.corpus import stop_words
from nltk.tokenize import RegexpTokenizer
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
        







