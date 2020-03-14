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
    vocab as vocabulario_controlado,
    termos_vocab as termos_vocabulario_controlado
)

from .custom_funcs import (
    create_vocabulary,
    plot_N_clusters,
    plot_dendrogram,
    plot_KMeans_inertia
)


# %%
# se o nltk der problema para rodar descomente essa parte
# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('rslp')

