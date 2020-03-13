# %%
from .config import (
    data_dir,
    dossies_path,
    respostas_path,
    dossies_metadados_path,
    respostas_metadados_path,
    vocabulario_controlado_path
)

from .data import (
    get_dossies_df,
    get_respostas_df,
    get_dossies_metadados_df,
    get_respostas_metadados_df,
    get_vocabulario_controlado,
    get_termos_vocabulario_controlado
)

from .custom_funcs import (
    create_vocabulary,
    plot_SVD_clusters,
    plot_dendrogram,
    plot_KMeans_inertia
)


# %%
# se o nltk der problema para rodar descomente essa parte
# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('rslp')

