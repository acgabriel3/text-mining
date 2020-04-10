import numpy as np
import pandas as pd
from src.features.build_features import get_tf_features
from src.models import train_model


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
        metadados.index.intersection(np.where(labels == cluster_alvo)[0])
    ])


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


def print_topics_by_doc(df, n_top_words=10, n_topics=100, n_top_topics=3, **kwargs):
    """
    imprime as top words para cada tópico de cada documento presente no df.

    Parameters
    ----------
    df : `pd.DataFrame`

    n_top_words : `int`
        quantidade de palavras para cada tópico

    n_topics : `int`
        quantidade de tópicos a serem buscados

    n_top_topics : `int`
        quantidade de top tópicos para imprimir as top_n_words

    **kwargs:
        lista de parametros para serem passados para o construtor do lda
    Returns
    -------
    `void`
    """
    X, feature_names = get_tf_features(df.conteudo)
    lda = train_model.lda(X, n_topics, **kwargs)
    doc_topic = lda.transform(X)

    for n in range(doc_topic.shape[0]):
        top_n_topics_indexes = doc_topic[n].argsort()[:-n_top_topics - 1:-1]
        print(f"doc: {df.nome_do_arquivo.iloc[n]}")
        print(
            f"\ttop {n_top_topics} topics indexes: {top_n_topics_indexes}")
        top_n_topics = lda.components_[top_n_topics_indexes]
        for topic_idx, topic in enumerate(top_n_topics):
            text = f'\t\tTopic #{top_n_topics_indexes[topic_idx]}: '
            text += ' '.join([feature_names[i]
                              for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(text)


def get_topics_by_doc(df, n_top_words=10, n_topics=200, n_top_topics=3, **kwargs):
    """
    retorna um dataframe com os topicos para cada documento

    Parameters
    ----------
    df : `pd.DataFrame`

    n_top_words : `int`
        quantidade de palavras para cada tópico

    n_topics : `int`
        quantidade de tópicos a serem buscados

    n_top_topics : `int`
        quantidade de top tópicos para imprimir as top_n_words

    **kwargs:
        lista de parametros para serem passados para o construtor do lda
    Returns
    -------
    `pd.DataFrame`
    """
    X, feature_names = get_tf_features(df.conteudo)
    lda = train_model.lda(X, n_topics, **kwargs)
    doc_topic = lda.transform(X)

    data = []
    for n in range(doc_topic.shape[0]):
        top_n_topics_indexes = doc_topic[n].argsort()[:-n_top_topics - 1:-1]
        top_n_topics = lda.components_[top_n_topics_indexes]

        data.append([
            df.nome_do_arquivo.iloc[n],
            [
                ' '.join(
                    [feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]
                ) for topic in top_n_topics
            ]
        ])

    return pd.DataFrame(
        data=data,
        columns=['documento', 'topicos_provaveis']
    )
