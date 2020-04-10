from src.data.make_dataset import load_respostas_df
from src.data.make_metadados import load_respostas_metadados_df
from src.features.build_features import get_tfidf_features, get_tf_features
from src.models import train_model, predict_model, validate_model
from src.visualization.visualize import plot_dendrogram_Agglomerative, plot_dendrogram, show
from src.data.make_reports import export_df_to_json, export_df_to_csv


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

    respostas_metadados = load_respostas_metadados_df(
        respostas.nome_do_arquivo)
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
        p=10,
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

    for cluster_index in range(1, n_clusters + 1):
        cluster_n = validate_model.checar_categoria(
            respostas_com_metadados, labels, cluster_index)
        print(f'documentos pertencentes ao grupo {cluster_index} - info')
        cluster_n.info()
        logger([
            {
                'name': f'documentos pertencentes ao grupo {cluster_index} - head',
                'value': cluster_n.head()
            },
        ])
        doc_topics_cluster_n = validate_model.get_topics_by_doc(cluster_n)
        export_df_to_csv(
            doc_topics_cluster_n, f'cluster_{cluster_index}',
            parent_path='topicos_por_cluster_e_documento',
            index=False
        )
        validate_model.print_topics_by_doc(cluster_n, n_top_topics=1)

    # para que as imagens sejam plotadas
    show()


if __name__ == "__main__":
    main()
