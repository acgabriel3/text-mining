import pandas as pd
from os import listdir
from os.path import isfile, join
import spacy 
from spacy import displacy

nlp = spacy.load('pt')


path = "D:/curso_ciencia_da_computacao/pesquisa com Prof.Ricardo/text-mining/dados/sbrt_txts/dossies"
files = [ f for f in listdir(path) if isfile(join(path,f)) ]

dossies = pd.DataFrame(data = None, columns = ['dossie', 'texto'])

for file in files:
    with open(file) as f:
        global text
        text = f.readlines()
        aux = pd.DataFrame(data = [[file, text]], columns = ['dossie', 'texto'])
        dossies = pd.DataFrame.append(dossies, aux, ignore_index = True) 


#Demora bastante para rodar e sobe bastante o uso da memoria ram
#dossies['texto'] = dossies['texto'].apply(lambda x : nlp(str(x))) 

teste = nlp(str(dossies['texto'][0]))

displacy.render(teste, style='dep', jupyter=False, options={'distance': 70}) #trocar ide, nao hah como utilizar no spyder





