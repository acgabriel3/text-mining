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
    pasta 'data/processed/vocabulario_controlado_geral.xlsx'

    Returns
    -------
    `pd.DataFrame`:
        contendo informações sobre todos os termos disponiveis
    """
    return pd.read_excel(open(vocabulario_controlado_path, mode='rb'), header=1)


def load_termos_vocabulario_controlado():
    """
    Carrega o nome dos termos que estão no vocabulário controlado.

    Este vocabulário controlado foi disponibilizado pelo sbrt e deve estar na
    pasta 'data/processed/vocabulario_controlado.html'.

    Returns
    -------
    `np.array`:
        contendo o nome de todas as palavras encontrados no nome dos termos
    """
    termos = vocab.voc_termo.loc[
        np.where(vocab.voc_termo.isnull() == False)
    ]

    tokens = np.array([
        nltk.word_tokenize(
            re.sub(r'[\W+]', ' ', termo_str).lower(),
            language='portuguese'
        )
        for termo_str in termos
    ])

    no_stop_word_termos = np.array([
        np.array([
            word for word in t if word
            not in nltk.corpus.stopwords.words('portuguese')
        ]) for t in tokens
    ])

    def aplicar_filtro(termo_str):
        termo_filtrado = re.sub(r'\d+', '', termo_str)
        termo_filtrado = re.sub(r'\s{2,}', ' ', termo_filtrado).strip()
        return termo_filtrado if len(termo_filtrado) > 1 else np.nan

    ret = np.array([])
    for a in no_stop_word_termos:
        ret = np.append(ret, [aplicar_filtro(v) for v in a])

    ret = np.sort(np.unique(ret))
    return ret[np.where(ret != 'nan')]


def load_dossies_metadados_df(arquivos, metadados=None) -> pd.DataFrame:
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
        contendo os metadados de cada dossie
    """
    nomes = _get_files(arquivos)
    json_metadados = json.loads(
        " ".join(open(dossies_metadados_path).readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        meta_src = _extrair_chaves_json(json_metadados, metadados, fn)
        if meta_src != None:
            data = [
                [*[json_metadados[fn][metadado_key]
                    for metadado_key in meta_src], f'{fn}.txt']
            ]
            row = pd.DataFrame(data=np.array(data), columns=[*meta_src, 'nome_do_arquivo'])
            df = df.append(row, ignore_index=True)
        else:
            print(f'nao ha metadados para o arquivo {fn}.txt')
    return df


def load_respostas_metadados_df(arquivos, metadados=None) -> pd.DataFrame:
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
        contendo os metadados de cada resposta técnica
    """
    nomes = _get_files(arquivos)
    json_metadados = json.loads(
        " ".join(open(respostas_metadados_path).readlines()))
    df = pd.DataFrame()
    for fn in nomes:
        meta_src = _extrair_chaves_json(json_metadados, metadados, fn)
        if meta_src != None:
            data = [
                [*[json_metadados[fn][metadado_key]
                    for metadado_key in meta_src], f'{fn}.txt']
            ]
            row = pd.DataFrame(data=np.array(data), columns=[*meta_src, 'nome_do_arquivo'])
            df = df.append(row, ignore_index=True)
        else:
            print(f'nao ha metadados para o arquivo {fn}.txt')
    return df


def _extrair_chaves_json(json, metadados, nome_do_arquivo):
    try:
        json[nome_do_arquivo]
        return metadados if metadados is not None else json[nome_do_arquivo].keys()
    except KeyError as ke:
        return None


def _get_files(arquivos):
    ext = '.txt'
    nomes = arquivos[[(lambda fn: False if fn.find(ext) < 0 else True)(f)
                      for f in arquivos]]
    return np.vectorize(lambda fn: fn[:-len(ext)])(nomes)


vocab = load_vocabulario_controlado()
termos_vocab = load_termos_vocabulario_controlado()
