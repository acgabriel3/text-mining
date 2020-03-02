# %%
import nltk
import pandas as pd
import string


# %%
df = pd.DataFrame(data=[
    ['Chegada do coronavírus desafia o sistema brasileiro de saúde', 'saude publica'],
    ['Mundo se mobiliza por uma vacina contra o Covid-19, o novo coronavírus', 'saude publica'],
    ['Coronavírus: Segundo caso do Brasil é confirmado em São Paulo', 'saude publica'],
    ['Multidão no Irã ateia fogo em hospital que atende pacientes com coronavírus', 'saude publica'],

    ['Apaixonado por carnaval, passista de quase 80 anos busca o samba todos os sábados no Centro de Florianópolis', 'carnaval'],
    ['Quarto suspeito de matar homem após festa de carnaval em União é preso', 'carnaval'],
    ['"TUDO OK": veja o passo a passo da coreografia do hit do carnaval', 'carnaval'],
    ['Blocos líricos se reúnem para desfile de despedida do carnaval em Olinda', 'carnaval'],
], columns=['text', 'tipo_noticia'])

df


# %%
def create_vocabulary(words):
    d = {}
    counter = 1

    def update_dict(d, w, c):
        d[w] = counter
        return d

    def f(w, counter, d=d): return d if w in d else update_dict(d, w, counter)

    for w in words:
        f(w, counter)
        counter = counter + 1

    return d


# %%
stop_words = nltk.corpus.stopwords.words('portuguese')
stemmer = nltk.stem.RSLPStemmer()

titulos = df.text.str.cat(sep=' ')

# remove pontuação da forma mais eficiente possivel
no_punct_txt = titulos.translate(str.maketrans('', '', string.punctuation))
no_punct_txt


# %%
tokens = nltk.word_tokenize(no_punct_txt.lower(), language='portuguese')
tokens


# %%
no_stop_words_txt = " ".join(
    [word for word in tokens if word not in stop_words])
no_stop_words_txt


# %%
stemmed_txt = "".join([stemmer.stem(word) for word in no_stop_words_txt])
stemmed_txt
