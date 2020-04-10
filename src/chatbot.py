import re
import string
import nltk
from src.data.make_metadados import termos_vocab
from src.data.make_dataset import load_dossies_df, load_respostas_df
from src.data.make_metadados import load_dossies_metadados_df, load_respostas_metadados_df
from src.features.build_features import get_tfidf_features, get_tf_features
from src.models import train_model, validate_model


class ChatBot:
    def get_documents(self, query):
        return ['Plantação de cacau', 'Cultivo de manga']
    pass


def pre_process_user_input(q):
    # remove pontuação da forma mais eficiente possivel
    q = q.translate(str.maketrans(' ', ' ', string.punctuation)).lower()

    tokens = nltk.word_tokenize(q, language='portuguese')

    no_stop_word_tokens = [
        word for word in tokens if word not in nltk.corpus.stopwords.words('portuguese')
    ]

    return " ".join(
        [word for word in no_stop_word_tokens if word in termos_vocab]
    )


def main():
    chatbot = ChatBot()
    while True:
        try:
            q = input('Usuário: ')
            q = pre_process_user_input(q)
            print(f'query = {q}')
            docs = chatbot.get_documents(q)
            if docs != None:
                print(
                    f'Bot: Achei esses documentos que estão relacionados com sua pesquisa {docs}')
            else:
                print('Não consegui encontrar nada')
        except(KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == "__main__":
    dossies = load_dossies_df()
    # respostas = load_respostas_df()

    dossies_metadados = load_dossies_metadados_df(dossies.nome_do_arquivo)
    # respostas_metadados = load_respostas_metadados_df(respostas.nome_do_arquivo)

    dossies_tf_X, dossies_feature_names = get_tf_features(dossies.conteudo)
    # respostas_tf_X, respostas_feature_names = get_tf_features(
    #     respostas.conteudo)

    n_topics = 200
    n_top_words = 10
    dossies_lda = train_model.lda(dossies_tf_X, n_topics)

    doc_topic = dossies_lda.transform(dossies_tf_X)
    # respostas_lda = train_model.lda(respostas_tf_X, n_topics)

    dossies_top_words = [
        [(i, dossies_feature_names[i])
         for i in topic.argsort()[:-n_top_words - 1:-1]]
        for topic in dossies_lda.components_
    ]

    validate_model.print_topics_by_doc(dossies)

    # respostas_top_words = [
    #     respostas_feature_names[i]
    #     for i in topic.argsort()[:-n_top_words - 1:-1]
    #     for topic in respostas_lda.components_
    # ]

    # top_words = [*dossies_top_words, *respostas_top_words]

    # print(dossies_top_words)

    # main()
