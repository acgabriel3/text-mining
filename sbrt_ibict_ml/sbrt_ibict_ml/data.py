# %%
from sbrt_ibict_ml.sbrt_ibict_ml.custom_funcs import basic_pre_processing
from sbrt_ibict_ml.sbrt_ibict_ml.config import dossies_path, respostas_path
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np


# %%
def get_dossies_df(size=None, seed=None) -> pd.DataFrame:
    files = np.array([f for f in listdir(dossies_path)
                      if isfile(join(dossies_path, f))])
    np.random.seed(seed)
    np.random.shuffle(files)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(dossies_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_processing(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row)
    return df


# %%
def get_respostas_df(size=None, seed=None) -> pd.DataFrame:
    files = np.array([f for f in listdir(respostas_path)
                      if isfile(join(respostas_path, f))])
    np.random.seed(seed)
    np.random.shuffle(files, )
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(respostas_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_processing(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row)
    return df
