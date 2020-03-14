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
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


# %%
df = pd.DataFrame(data=[
    ['Mundo se mobiliza por uma vacina contra o Covid-19, o novo coronavírus', 'saude publica'],
    ['Coronavírus: Segundo caso do Brasil é confirmado em São Paulo', 'saude publica'],
    ['Este desafio de inglês será fácil para quem entende de Carnaval', 'carnaval'],
    ['Monobloco desfila neste domingo de pós-carnaval no Rio; veja lista completa', 'carnaval'],
    ['Paciente com suspeita de coronavírus morre em Nova Friburgo (RJ)', 'saude publica'],
    ['Quarto suspeito de matar homem após festa de carnaval em União é preso', 'carnaval'],
    ['“Não há chá milagroso”, avisa infectologista sobre coronavírus', 'saude publica'],
    ['É fake! Loló e cocaína não curam coronavírus', 'saude publica'],
    ['Apaixonado por carnaval, passista de quase 80 anos busca o samba todos os sábados no Centro de Florianópolis', 'carnaval'],
    ['Anitta, a sensação deste Carnaval, desfilará em seu bloco no centro do Rio', 'carnaval'],
    ['Coronavírus: OMS reclassifica ameaça global para “muito elevada”', 'saude publica'],
    ['"TUDO OK": veja o passo a passo da coreografia do hit do carnaval', 'carnaval'],
    ['Blocos líricos se reúnem para desfile de despedida do carnaval em Olinda', 'carnaval'],
    ['Multidão no Irã ateia fogo em hospital que atende pacientes com coronavírus', 'saude publica'],
    ['Chegada do coronavírus desafia o sistema brasileiro de saúde', 'saude publica'],
    ['Acabou o Carnaval: 10 frases para voltar ao trabalho depois do feriado', 'carnaval'],
    ['Coronavírus: Itália registra 29 mortes e 1.049 casos confirmados', 'saude publica'],
    ['Estas são as dicas para uma folia de Carnaval sem erros, segundo professor', 'carnaval'],
], columns=['text', 'tipo_noticia'])

df


# %%
stop_words = stopwords.words('portuguese')


# %%
X_train, X_test, y_train, y_test = train_test_split(
    df.text.values, df.tipo_noticia, test_size=.3)

count_vect = CountVectorizer(stop_words=stop_words)
X_train_counts = count_vect.fit_transform(X_train)
X_train_counts.shape


# %%
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape


# %%
clf = MultinomialNB().fit(X_train_tfidf, y_train)


# %%
def get_prediction_for(model, docs):
    X_counts = count_vect.transform(docs)
    X_tfidf = tfidf_transformer.transform(X_counts)

    return model.predict(X_tfidf)


# %%
new_docs = ['Bolsonaro é alfinetado em desfile de escolas de samba no Rio',  # carnaval
            'Gripe matou 37 pessoas no Distrito Federal em 2019',  # saude publica
            'Coronavírus: estados estudam suspender cirurgias e tratamentos',  # saude publica
            'Megablocos concentram público e patrocínio e encarecem carnaval de SP',  # carnaval
            'Com superlotação, Hospital de Santa Maria restringe atendimentos',  # saude publica
            'Fantasias indígenas e com referências à África levantam debate no Carnaval',  # carnaval
            'Brasileiros sequenciam genoma do coronavírus em 48 horas',  # saude publica
            'Brasil confirma segundo caso de coronavírus, também em São Paulo',  # saude publica
            'Não vai pular Carnaval? Estes serão ótimos dias para procurar emprego',  # carnaval
            'Brasil tem 252 casos suspeitos de coronavírus e dois confirmados']  # saude publica
y_test_pred = get_prediction_for(clf, X_test)
y_new_pred = get_prediction_for(clf, new_docs)


# %%
pd.DataFrame(data={'text': X_test, 'label': y_test,
                   'predicted': y_test_pred}, columns=['text', 'label', 'predicted'])


# %%
metrics.confusion_matrix(
    y_test, y_test_pred, labels=np.unique(df.tipo_noticia))


# %%
pd.DataFrame(data={'text': new_docs, 'predicted': y_new_pred},
             columns=['text', 'predicted'])
