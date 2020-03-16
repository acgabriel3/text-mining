import numpy as np


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
    `np.array`:
        lista das categorias de cada documento pertencente ao cluster alvo
    """
    return np.array([
        cat for cat in metadados.loc[
            np.where(labels == cluster_alvo)
        ].categoria
    ])
