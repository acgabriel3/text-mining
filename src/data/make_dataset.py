import numpy as np
from os.path import join
import pandas as pd
from src.data.preprocess import basic_pre_process, _load_files
from src.data.paths import interim_dossies_path, interim_respostas_path


def load_dossies_df(size=None, seed=None) -> pd.DataFrame:
    """
    Carrega os dossies em uma estrutura de DataFrame.

    Dado que os dossies já foram pré processados, então popula um DataFrame com os mesmos.

    Parameters
    ----------
    size : `int`
        tamanho da amostra de dossies que serão selecionados. Caso não seja
        especificado, então todos os documentos serão carregados.

    seed : `str`
        seed para selecionar uma amostra aleatória de dossies.

    Returns
    -------
    `pd.DataFrame`:
        um DataFrame que contém o nome do arquivo e o texto pré-processado
    """
    files = _load_files(interim_dossies_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        df = _popular_df(df, file, interim_dossies_path)
    return df


def load_respostas_df(size=None, seed=None) -> pd.DataFrame:
    """
    Carrega os dossies em uma estrutura de DataFrame.

    Dado que os dossies já foram pré processados, então popula um DataFrame com os mesmos.

    Parameters
    ----------
    size : int
        tamanho da amostra de dossies que serão selecionados. Caso não seja
        especificado, então todos os documentos serão carregados.

    seed : str
        seed para selecionar uma amostra aleatória de dossies.

    Returns
    -------
    `pd.DataFrame`:
        um DataFrame que contém o nome do arquivo e o texto pré-processado
    """
    files = _load_files(interim_respostas_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        df = _popular_df(df, file, interim_respostas_path)
    return df


def _popular_df(df, nome_arquivo, path) -> pd.DataFrame:
    # necessário setar o enconding pra conseguir ler de forma correta os caracteres
    doc = open(join(path, nome_arquivo),
               errors='replace', encoding='cp1252')
    row = pd.DataFrame(
        data=[
            [nome_arquivo, " ".join(doc.readlines())]
        ], columns=['file', 'text'])
    return df.append(row, ignore_index=True)
