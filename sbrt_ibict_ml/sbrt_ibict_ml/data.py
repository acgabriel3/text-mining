# %%
from sbrt_ibict_ml.sbrt_ibict_ml.config import (
    dossies_path,
    respostas_path,
    dossies_metadados_path,
    respostas_metadados_path,
    vocabulario_controlado_path
)
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import json
import re
import string
import nltk


# %%
def get_files(path, seed):
    files = np.array([f for f in listdir(path)
                      if isfile(join(path, f))])
    np.random.seed(seed)
    np.random.shuffle(files)
    return files


# %%
def get_vocabulario_controlado():
    content = "".join(open(vocabulario_controlado_path,
                           encoding='cp1252').readlines())
    soup = BeautifulSoup(content, 'html.parser')
    values = soup.find_all('span', class_='style6')
    vocabs = []
    offset = 15
    for i in range(0, len(values) - offset, offset):
        vocabs.append(
            tuple(re.sub(r'\s{2,}', '', v.text).lower().strip()
                  for v in values[i:i+offset])
        )
    return vocabs


vocab = get_vocabulario_controlado()


# %%
def get_termos_vocabulario_controlado():
    return [t[1] for t in vocab[1:]]


termos_vocab = get_termos_vocabulario_controlado()


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

    no_stop_word_tokens = [
        word for word in tokens if word not in [
            stop_words, 'copyright', '©', 'sbrt', 'httpwwwsbrtibictbr', "˙˘˙"
        ]
    ]

    return " ".join(np.unique([word for word in no_stop_word_tokens if word in termos_vocab]))
    # return "".join([stemmer.stem(word) for word in no_stop_words_txt])


# %%
def get_dossies_df(size=None, seed=None) -> pd.DataFrame:
    files = get_files(dossies_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(dossies_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_processing(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row, ignore_index=True)
    return df


# %%
def get_respostas_df(size=None, seed=None) -> pd.DataFrame:
    files = get_files(respostas_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(respostas_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_processing(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row, ignore_index=True)
    return df


# %%
def get_dossies_metadados_df(arquivos):
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    nomes = np.vectorize(lambda fn: fn[:-len(ext)])(nomes)
    metadados = json.loads(
        " ".join(open(dossies_metadados_path).readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        row = pd.DataFrame(
            data=[
                [metadados[fn]['titulo'], metadados[fn]
                    ['palavras_chave'], metadados[fn]['categoria']]
            ], columns=['titulo', 'palavras_chave', 'categoria'])
        df = df.append(row, ignore_index=True)
    return df


# %%
def get_respostas_metadados_df(arquivos):
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    nomes = np.vectorize(lambda fn: fn[:-len(ext)])(nomes)
    metadados = json.loads(
        " ".join(open(respostas_metadados_path).readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        data = []

        try:
            metadados[fn]
            data = [
                [metadados[fn]['titulo'], metadados[fn]['palavras_chave']]
            ]
        except KeyError as ke:
            data = [
                ['null', []]
            ]

        row = pd.DataFrame(data=data, columns=['titulo', 'palavras_chave'])
        df = df.append(row, ignore_index=True)
    return df
