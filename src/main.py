from src.data.make_dataset import load_dossies_df
from src.data.make_metadados import load_dossies_metadados_df
from src.features.build_features import get_tfidf_features
from src.models import train_model, predict_model
from src.visualization.visualize import plot_dendrogram_Agglomerative, plot_dendrogram, show


def main():
    dossies = load_dossies_df(size=50)
    print(dossies.head())

    dossies_metadados = load_dossies_metadados_df(
        dossies.file, ['titulo', 'palavras_chave', 'categoria'])
    print(dossies_metadados.head())

    X = get_tfidf_features(dossies.text)
    print(X.shape)

    aggl_clustering = train_model.agglomerative(
        X, distance_threshold=0, n_clusters=None, linkage='average')
    print(aggl_clustering)

    plot_dendrogram_Agglomerative(aggl_clustering)
    plot_dendrogram(X, method='ward')

    print([c for c in dossies_metadados.loc[[13, 44]].categoria])
    show()


if __name__ == "__main__":
    main()
