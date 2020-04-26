import math
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from elasticsearch import Elasticsearch
from src.data.paths import dialogos_basicos_path, solicitacoes_path

es = Elasticsearch()

_DEV = True

if _DEV:
    logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    'Sara',
    # storage_adapter='chatterbot.storage.SQLStorageAdapter',
    # database="teste",
)
trainer = ListTrainer(chatbot)

trainer.train('chatterbot.corpus.portuguese')


def train_from_elasticsearch_response(q, top_words=None):
    res = es.search(index="sentencas_sbrt", body={
        "query": {
            "match": {
                "sentenca": {
                    "query": q
                }
            }
        }
    })

    if _DEV:
        print([hit['_source']['sentenca'] for hit in res['hits']['hits']])

    for hit in res['hits']['hits']:
        if len(hit['_source']['sentenca'].split()) > 1:
            trainer.train([q, hit['_source']['sentenca']])


def train_from_builtin_data(path):
    data = json.loads(open(path, 'r').read())
    train = []
    for row in data:
        train.append(row['question'])
        train.append(row['answer'])
    trainer.train(train)


def main():
    train_from_builtin_data(dialogos_basicos_path)
    # train_from_builtin_data(solicitacoes_path) # tem as respostas em branco
    while True:
        try:
            question = input('Usuário: ')
            answer = chatbot.get_response(question.lower())

            query = False if answer.confidence >= .5 else True
            if query:
                # pegar as top_words?
                train_from_elasticsearch_response(question)
                answer = chatbot.get_response(question.lower())

            print(f'{chatbot.name}: {answer}')

            # txt = str(answer)
            # idx = math.floor(train.index(txt) / 2)
            # for i, val in enumerate(tag):
            #     if val == 'consulta':
            #         query = True
            #         break
            #     if i == idx:
            #         break
        except(KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == "__main__":
    main()
