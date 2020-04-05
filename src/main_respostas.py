from src.data.make_dataset import load_respostas_df
from src.data.make_metadados import load_respostas_metadados_df
from src.features.build_features import get_tfidf_features, get_tf_features
from src.models import train_model, predict_model, validate_model
from src.visualization.visualize import plot_dendrogram_Agglomerative, plot_dendrogram, show


def logger(infos):
    print('*' * 50)
    for info in infos:
        print(info['name'] + ':')
        print(info['value'])
        print()
    print('*' * 50)


def main():
    respostas = load_respostas_df()
    logger([
        {
            'name': 'len respostas',
            'value': len(respostas)
        },
        {
            'name': 'respostas head',
            'value': respostas.head()
        }
    ])

    respostas_metadados = load_respostas_metadados_df(respostas.nome_do_arquivo)
    logger([
        {
            'name': 'len metadados dos respostas',
            'value': len(respostas_metadados)
        },
        {
            'name': 'metadados dos respostas head',
            'value': respostas_metadados.head()
        }
    ])

    tfidf_X, tfidf_feature_names = get_tfidf_features(respostas.conteudo)
    tf_X, tf_feature_names = get_tf_features(respostas.conteudo)
    logger([
        {
            'name': 'Tf idf sparse matrix shape',
            'value': tfidf_X.shape
        },
        {
            'name': 'Tf sparse matrix shape',
            'value': tf_X.shape
        },
    ])

    aggl_clustering = train_model.agglomerative(
        tfidf_X, distance_threshold=0, n_clusters=None, linkage='ward')
    logger([
        {
            'name': 'Aglomerattive clustering object',
            'value': aggl_clustering
        },
    ])

    n_topics = 5
    n_top_words = 10
    print(f'top {n_top_words} words for {n_topics} topics using LDA')
    validate_model.print_top_words(
        train_model.lda(tf_X, n_topics),
        tf_feature_names,
        n_top_words=n_top_words
    )
    print(f'top {n_top_words} words for {n_topics} topics using NMF')
    validate_model.print_top_words(
        train_model.nmf(tfidf_X, n_topics),
        tfidf_feature_names,
        n_top_words=n_top_words
    )

    plot_dendrogram_Agglomerative(
        aggl_clustering,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=100,  # show only the last p merged clusters
        leaf_rotation=90,
        # leaf_font_size=12.,
        show_contracted=True
    )

    Z = train_model.linkage_matrix(tfidf_X, method='ward')
    plot_dendrogram(
        Z,
        truncate_mode='level',
        p=5,
        leaf_rotation=90,
        # leaf_font_size=12.,
        show_contracted=True
    )

    # a partir da analise do dendrograma plotada, 5 clusters parece uma
    # boa escolha
    n_clusters = 5
    labels = predict_model.Z_labels(Z, t=n_clusters, criterion='maxclust')
    logger([
        {
            'name': 'labels of documents using linkage method',
            'value': labels
        }
    ])

    respostas_com_metadados = respostas.join(
        respostas_metadados.set_index('nome_do_arquivo'),
        on='nome_do_arquivo'
    ).dropna()

    logger([
        {
            'name': 'len respostas que possuem metadados',
            'value': len(respostas_com_metadados)
        },
        {
            'name': 'respostas que possuem metadados head',
            'value': respostas_com_metadados.head()
        }
    ])

    # Com os resultados dessa célula pode-se presumir que documentos com a
    # label 2 está fortemente relacionado à questões de agricultura e com
    # vários registros sobre cultivo
    cluster_2 = validate_model.checar_categoria(
        respostas_com_metadados, labels, 2)
    print('documentos pertencentes ao grupo 2 - info')
    cluster_2.info()
    logger([
        {
            'name': 'documentos pertencentes ao grupo 2 - head',
            'value': cluster_2.head()
        },
        {
            'name': 'documentos que possuem a palavra "cultivo" no titulo',
            'value': validate_model.checar_substring(cluster_2, 'titulo', 'cultivo')
        }
    ])

    # Com os resultados dessa célula pode-se presumir que documentos com a
    # label 1 está fortemente relacionado à questões de agricultura e cogumelos
    cluster_1 = validate_model.checar_categoria(
        respostas_com_metadados, labels, 1)
    print('documentos pertencentes ao grupo 1 - info')
    cluster_1.info()
    logger([
        {
            'name': 'documentos pertencentes ao grupo 1 - head',
            'value': cluster_1.head()
        },
        {
            'name': 'documentos que possuem a palavra "cogumelo" ou "cogumelos" no titulo',
            'value': validate_model.checar_substring(cluster_1, 'titulo', r'cogumelos?')
        }
    ])

    # # para que as imagens sejam plotadas
    show()


if __name__ == "__main__":
    main()
