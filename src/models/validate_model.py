import numpy as np
import pandas as pd


def checar_categoria(metadados, labels, cluster_alvo):
    """
    Checa se as labels encontradas correspondem com as disponiveis nos metadados.

    Estes metadados devem ser baixados e colocados na pasta
    'data/processed/[dossies|respostas]_metadados.json'

    Parameters
    ----------
    metadados : `pd.Dataframe`
        contendo as informações dos metadados 

    labels : `list` of : `int`
        indices dos cluster, de forma que o documento i pertença ao cluster
        indicado na posição labels[i]

    cluster_alvo : `int`
        indice do cluster o qual deseja-se comparar os metadados

    Returns
    -------
    `pd.DataFrame`:
        dataframe contendo informações das categorias e titulo de cada
        documento pertencente ao cluster alvo
    """
    return pd.DataFrame(data=metadados.loc[
        np.where(labels == cluster_alvo)][['titulo', 'categoria']]
    )


def checar_substring(df, coluna, substring):
    """
    retorna um subconjunto do df original, o qual possui os registros que
    tenham a substring na coluna

    Parameters
    ----------
    df : `pd.Dataframe`

    coluna : `str`
        coluna na qual deve ser feita a pesquisa pela substring

    substring : `str`
        substring que deve ser procurada

    Returns
    -------
    `pd.DataFrame`:
        um subconjunto do dataframe passado no qual satisfaça a condição de que
        a substring existe na coluna passada
    """
    return df[df[coluna].str.contains(substring, case=False)]
