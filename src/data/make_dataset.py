import numpy as np
from os.path import isfile, join
from os import listdir
import pandas as pd
from .preprocess import basic_pre_process
from .paths import dossies_path, respostas_path


def load_files(path, seed):
    files = np.array([f for f in listdir(path)
                      if isfile(join(path, f))])
    np.random.seed(seed)
    np.random.shuffle(files)
    return files


def load_dossies_df(size=None, seed=None) -> pd.DataFrame:
    files = load_files(dossies_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(dossies_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_process(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row, ignore_index=True)
    return df


def load_respostas_df(size=None, seed=None) -> pd.DataFrame:
    files = load_files(respostas_path, seed)
    df = pd.DataFrame()
    for file in files if size == None else files[0:size]:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        dossie = open(join(respostas_path, file),
                      errors='replace', encoding='cp1252')
        row = pd.DataFrame(
            data=[
                [file, basic_pre_process(" ".join(dossie.readlines()))]
            ], columns=['file', 'text'])
        df = df.append(row, ignore_index=True)
    return df
