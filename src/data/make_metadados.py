from bs4 import BeautifulSoup
from os.path import join
import pandas as pd
import numpy as np
import json
import re
import nltk
from src.data.paths import (
    vocabulario_controlado_path,
    dossies_metadados_path,
    respostas_metadados_path
)


def load_vocabulario_controlado():
    """
    Carrega os dados do vocabulario controlado.

    Este vocabulário controlado foi disponibilizado pelo sbrt e deve estar na
    pasta 'data/processed/vocabulario_controlado.html'

    Os termos possuem o formato: (
        ID, TERMO, NOTA, USADO_PARA, USE, USE_COM, VER_TAMBÉM, ESPECIFICADOR,
        INCLUSÃO, ATUALIZAÇÃO, STATUS, RT, APROVADOR, SUGERIDO_POR,
        INSTITUIÇÃO
    )

    Returns
    -------
    `list` of `Termo`:
        Uma lista de tuplas contendo informações sobre todos os termos relevantes 
    """
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
    """
    Carrega o nome dos termos que estão no vocabulário controlado.

    Este vocabulário controlado foi disponibilizado pelo sbrt e deve estar na
    pasta 'data/processed/vocabulario_controlado.html'.

    Returns
    -------
    `np.array`:
        contendo o nome de todos os termos do vocabulario controlado tokenizados
    """
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

    return np.unique(ret)


def load_dossies_metadados_df(arquivos, metadados) -> pd.DataFrame:
    """
    Carrega os metadados dos dossies em uma estrutura de DataFrame.

    Estes metadados devem ser baixados e colocados na pasta
    'data/processed/[dossies|respostas]_metadados.json'

    Parameters
    ----------
    arquivos : `list` of : `str`
        contendo o nome dos arquivos

    metadados : `list` of : `str` 
        contendo o nome dos metadados que devem ser extraídos do json.
        Possíveis valores: ['cnae_asunto', 'categoria', 'palavras_chave',
        'resumo', 'data', 'instituicao_responsavel', 'assunto', 'titulo',
        'cnae_dossie']

    Returns
    -------
    `pandas.DataFrame`:
        um DataFrame que contém o nome do arquivo e o texto pré-processado
    """
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


def load_respostas_metadados_df(arquivos, metadados) -> pd.DataFrame:
    """
    Carrega os metadados das respostas em uma estrutura de DataFrame.

    Estes metadados devem ser baixados e colocados na pasta
    'data/processed/respostas_metadados.json'

    Parameters
    ----------
    arquivos : `list` of : `str`
        contendo o nome dos arquivos

    metadados : `list` of : `str` 
        contendo o nome dos metadados que devem ser extraídos do json.
        Possíveis valores: ['cnae_asunto', 'categoria', 'palavras_chave',
        'resumo', 'data', 'instituicao_responsavel', 'assunto', 'titulo',
        'cnae_dossie']

    Returns
    -------
    `pandas.DataFrame`:
        um DataFrame que contém o nome do arquivo e o texto pré-processado
    """
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    nomes = np.vectorize(lambda fn: fn[:-len(ext)])(nomes)
    json_metadados = json.loads(
        " ".join(open(respostas_metadados_path).readlines()))
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


vocab = load_vocabulario_controlado()
termos_vocab = load_termos_vocabulario_controlado()
