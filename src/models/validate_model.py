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


def print_top_words(model, feature_names, n_top_words):
    """
    imprime as top words para cada tópico do model.

    Parameters
    ----------
    model : `sklearn.decomposition.NMF` | `sklearn.decomposition.LDA`

    feature_names : `list` of `str`
        vocabulário do TfidfVectorizer para o NMF ou do CountVectorizer para o LDA

    n_top_words : `int`
        quantidade de palavras para cada tópico

    Returns
    -------
    `void`
    """
    for topic_idx, topic in enumerate(model.components_):
        message = f'Topic #{topic_idx}: '
        message += ' '.join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()
