from bs4 import BeautifulSoup
from os.path import join
import pandas as pd
import numpy as np
import json
import re
import nltk
from .paths import vocabulario_controlado_path, dossies_metadados_path, respostas_metadados_path


def load_vocabulario_controlado():
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


def load_termos_vocabulario_controlado():
    termos = np.array([t[1] for t in vocab[1:]])
    tokens = np.array([
        nltk.word_tokenize(termo, language='portuguese') for termo in termos
    ])
    no_stop_word_termos = np.array([
        np.array([
            word for word in t if word
            not in nltk.corpus.stopwords.words('portuguese')
        ]) for t in tokens
    ])

    ret = np.array([])
    for a in no_stop_word_termos:
        ret = np.append(ret, [re.sub(r'\d+', '', v) for v in a])

    return ret


def load_dossies_metadados_df(arquivos, metadados):
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    nomes = np.vectorize(lambda fn: fn[:-len(ext)])(nomes)
    json_metadados = json.loads(
        " ".join(open(dossies_metadados_path).readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        data = []

        try:
            json_metadados[fn]
            data = [
                [json_metadados[fn][metadado] for metadado in metadados]
            ]
        except KeyError as ke:
            data = [
                ['null' for m in metadados]
            ]

        row = pd.DataFrame(data=data, columns=metadados)
        df = df.append(row, ignore_index=True)
    return df


def load_respostas_metadados_df(arquivos):
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
                ['null' for m in metadados]
            ]

        row = pd.DataFrame(data=data, columns=['titulo', 'palavras_chave'])
        df = df.append(row, ignore_index=True)
    return df


vocab = load_vocabulario_controlado()
termos_vocab = load_termos_vocabulario_controlado()
