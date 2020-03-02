# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from nltk.corpus import stopwords
import string
import numpy as np

# Perform the necessary imports to build ML model
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
# tokenize and remove punctuation/stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from adjustText import adjust_text


# %%
X = [
    'Bolsonaro é alfinetado em desfile de escolas de samba no Rio',  # carnaval
    'Gripe matou 37 pessoas no Distrito Federal em 2019',  # saude
    'Coronavírus: estados estudam suspender cirurgias e tratamentos',  # saude
    'Megablocos concentram público e patrocínio e encarecem carnaval de SP',  # carnaval
    'Com superlotação, Hospital de Santa Maria restringe atendimentos',  # saude
    'Fantasias indígenas e com referências à África levantam debate no Carnaval',  # carnaval
    'Brasileiros sequenciam genoma do coronavírus em 48 horas',  # saude
    'Brasil confirma segundo caso de coronavírus, também em São Paulo',  # saude
    'Não vai pular Carnaval? Estes serão ótimos dias para procurar emprego',  # carnaval
    'Brasil tem 252 casos suspeitos de coronavírus e dois confirmados',  # saude
    'Mundo se mobiliza por uma vacina contra o Covid-19, o novo coronavírus',  # saude
    'Coronavírus: Segundo caso do Brasil é confirmado em São Paulo',  # saude
    'Este desafio de inglês será fácil para quem entende de Carnaval',  # carnaval
    'Monobloco desfila neste domingo de pós-carnaval no Rio; veja lista completa',  # carnaval
    # saude
    'Paciente com suspeita de coronavírus morre em Nova Friburgo (RJ)',
    'Quarto suspeito de matar homem após festa de carnaval em União é preso',  # carnaval
    '“Não há chá milagroso”, avisa infectologista sobre coronavírus',  # saude
    'É fake! Loló e cocaína não curam coronavírus',  # saude
    'Apaixonado por carnaval, passista de quase 80 anos busca o samba todos os sábados no Centro de Florianópolis',  # carnaval
    'Anitta, a sensação deste Carnaval, desfilará em seu bloco no centro do Rio',  # carnaval
    'Coronavírus: OMS reclassifica ameaça global para “muito elevada”',  # saude
    '"TUDO OK": veja o passo a passo da coreografia do hit do carnaval',  # carnaval
    'Blocos líricos se reúnem para desfile de despedida do carnaval em Olinda',  # carnaval
    'Multidão no Irã ateia fogo em hospital que atende pacientes com coronavírus',  # saude
    'Chegada do coronavírus desafia o sistema brasileiro de saúde',  # saude
    'Acabou o Carnaval: 10 frases para voltar ao trabalho depois do feriado',  # carnaval
    'Coronavírus: Itália registra 29 mortes e 1.049 casos confirmados',  # saude
    'Estas são as dicas para uma folia de Carnaval sem erros, segundo professor'  # carnaval
]

X

# %%
stop_words = stopwords.words('portuguese')


# %%
count_vect = CountVectorizer(stop_words=stop_words)
X_train_counts = count_vect.fit_transform(X)
X_train_counts.shape

# %%
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

# %%
clf = KMeans(n_clusters=2).fit(X_train_tfidf)


# %%
def get_prediction_for(model, docs):
    X_counts = count_vect.transform(docs)
    X_tfidf = tfidf_transformer.transform(X_counts)

    return model.predict(X_tfidf)


# %%
y_pred = get_prediction_for(clf, X)
y_real = [
    'carnaval',
    'saude',
    'saude',
    'carnaval',
    'saude',
    'carnaval',
    'saude',
    'saude',
    'carnaval',
    'saude',
    'saude',
    'saude',
    'carnaval',
    'carnaval',
    'saude',
    'carnaval',
    'saude',
    'saude',
    'carnaval',
    'carnaval',
    'saude',
    'carnaval',
    'carnaval',
    'saude',
    'saude',
    'carnaval',
    'saude',
    'saude'
]

# %%
df_res = pd.DataFrame(data={'text': X, 'labels': y_real, 'predicted': y_pred},
                      columns=['text', 'labels', 'predicted'])


# %%
pd.crosstab(df_res.predicted, df_res.labels)


# %%
pca = PCA(n_components=2)
scatter_plot_points = pca.fit_transform(X_train_counts.toarray())

colors = ["r", "b", "c", "y", "m"]


x_axis = [o[0] for o in scatter_plot_points]
y_axis = [o[1] for o in scatter_plot_points]
fig, ax = plt.subplots(figsize=(20, 10))

ax.scatter(x_axis, y_axis, c=[colors[d] for d in y_pred])

texts = [plt.text(x_axis[i], y_axis[i], X[i]) for i in range(len(x_axis))]

texts
adjust_text(texts)


# %%
