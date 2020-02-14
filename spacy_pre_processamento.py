import pandas as pd
from os import listdir
from os.path import isfile, join
import spacy 
from spacy import displacy
from collections import Counter

#tendo de usar as stop_words disponiveis no nltk
from nltk.corpus import stopwords

stop_words = stopwords.words('portuguese')

#nlp = spacy.load('pt', parse = True, tag = True, entity = True)
nlp = spacy.load('pt')

path = "D:/curso_ciencia_da_computacao/pesquisa com Prof.Ricardo/text-mining/dados/sbrt_txts/dossies"
files = [ f for f in listdir(path) if isfile(join(path,f)) ]

dossies = pd.DataFrame(data = None, columns = ['dossie', 'texto'])

for file in files:
    with open('dados/sbrt_txts/dossies/' + file) as f:
        global text
        text = f.readlines()
        aux = pd.DataFrame(data = [[file, text]], columns = ['dossie', 'texto'])
        dossies = pd.DataFrame.append(dossies, aux, ignore_index = True) 


#Demora bastante para rodar e sobe bastante o uso da memoria ram
#dossies['texto'] = dossies['texto'].apply(lambda x : nlp(str(x))) 

dossies['spacy'] = dossies['texto'].apply(lambda x: nlp(str(x)))

stop_words = Counter(stop_words)

def retira_stop_words(texto):
    lemmas = [token.lemma_ for token in texto.doc]
    texto_sem_stop_words = ''.join(lemma for lemma in lemmas if lemma.isalpha() and lemma not in stop_words)
    return texto_sem_stop_words

#displacy.render(teste, style='dep', jupyter=False, options={'distance': 70}) #trocar ide, nao hah como utilizar no spyder




