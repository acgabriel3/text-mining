# %%
from sbrt_ibict_ml.sbrt_ibict_ml.custom_funcs import basic_pre_processing
from sbrt_ibict_ml.sbrt_ibict_ml.config import dossies_path, respostas_path, data_dir
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import json


# %%
def get_files(path, seed):
    files = np.array([f for f in listdir(path)
                      if isfile(join(path, f))])
    np.random.seed(seed)
    np.random.shuffle(files)
    return files


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
        " ".join(open(data_dir / 'dossies_metadados.json').readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        row = pd.DataFrame(
            data=[
                [metadados[fn]['titulo'], metadados[fn]['palavras_chave']]
            ], columns=['titulo', 'palavras_chave'])
        df = df.append(row, ignore_index=True)
    return df


# %%
def get_respostas_metadados_df(arquivos):
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    nomes = np.vectorize(lambda fn: fn[:-len(ext)])(nomes)
    metadados = json.loads(
        " ".join(open(data_dir / 'respostas_metadados.json').readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        row = pd.DataFrame(
            data=[
                [metadados[fn]['titulo'], metadados[fn]['palavras_chave']]
            ], columns=['titulo', 'palavras_chave'])
        df = df.append(row, ignore_index=True)
    return df

