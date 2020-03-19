from src.visualization.visualize import plot_dendrogram_Agglomerative, plot_dendrogram, show
from src.models import train_model, predict_model, validate_model
from src.features.build_features import get_tfidf_features
from src.data.make_metadados import load_dossies_metadados_df
from src.data.make_dataset import load_dossies_df


def main():
    dossies = load_dossies_df()
    print(len(dossies))
    print(dossies.head())

    dossies_metadados = load_dossies_metadados_df(
        dossies.file, ['titulo', 'palavras_chave', 'categoria'])
    print(len(dossies_metadados))
    print(dossies_metadados.head())

    X = get_tfidf_features(dossies.text)
    print(X.shape)

    aggl_clustering = train_model.agglomerative(
        X, distance_threshold=0, n_clusters=None, linkage='ward')
    print(aggl_clustering)
    plot_dendrogram_Agglomerative(
        aggl_clustering,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=100,  # show only the last p merged clusters
        leaf_rotation=90,
        # leaf_font_size=12.,
        show_contracted=True
    )

    Z = train_model.linkage_matrix(X, method='ward')
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
    print(labels)

    # Com os resultados dessa célula pode-se presumir que documentos com a
    # label 2 está fortemente relacionado à questões de agricultura e com
    # vários registros sobre cultivo
    cluster_2 = validate_model.checar_categoria(dossies_metadados, labels, 2)
    print(cluster_2.info())
    print(cluster_2.head())
    print(validate_model.checar_substring(cluster_2, 'titulo', 'cultivo'))

    # Com os resultados dessa célula pode-se presumir que documentos com a
    # label 1 está fortemente relacionado à questões de agricultura e cogumelos
    cluster_1 = validate_model.checar_categoria(dossies_metadados, labels, 1)
    print(cluster_1.info())
    print(cluster_1.head())
    print(validate_model.checar_substring(cluster_1, 'titulo', r'cogumelos?'))

    # para que as imagens sejam plotadas
    show()


if __name__ == "__main__":
    main()
