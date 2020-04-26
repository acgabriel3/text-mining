import math
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from elasticsearch import Elasticsearch

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


def train_from_elasticsearch_response(q, top_words=None):
    res = es.search(index="sentencas_sbrt", body={
        "query": {
            "match": {
                "sentenca": {
                    "query": f'{q} {top_words}'
                }
            }
        }
    })

    if _DEV:
        print(hit['_source']['sentenca'] for hit in res['hits']['hits'])

    l = []
    for hit in res['hits']['hits']:
        l.append(q)
        l.append(hit['_source']['sentenca'])

    trainer.train(l)


def train_from_builtin_data():
    data = json.loads(open('dialogo.json', 'r').read())
    train = []
    tag = []
    for row in data:
        train.append(row['question'])
        train.append(row['answer'])
    for row in data:
        tag.append(row['flag'])
    trainer.train(train)


def main():
    train_from_builtin_data()
    while True:
        try:
            question = input('Usuário: ')
            answer = chatbot.get_response(question.lower())
            
            query = False if answer.confidence > .7 else True
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
