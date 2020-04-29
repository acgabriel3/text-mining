import math
import json
import logging
import time
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from elasticsearch import Elasticsearch
from src.data.paths import dialogos_basicos_path, solicitacoes_path

es = Elasticsearch()

_DEV = True

if _DEV:
    logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

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
                    "query": f'{q}'
                }
            }
        }
    })

    if _DEV:
        print([hit['_source']['sentenca'] for hit in res['hits']['hits']])

    list = []
    for hit in res['hits']['hits']:
    #    if len(hit['_source']['sentenca'].split()) > 1:
    #        trainer.train([q, hit['_source']['sentenca']])
        list.append([hit['_source']['sentenca']])

    return list

def train_from_builtin_data(path):
    data = json.loads(open(path, 'r').read())
    train = []
    for row in data:
        train.append(row['question'])
        train.append(row['answer'])
    trainer.train(train)

@app.route("/")
def home():    
    return render_template("home.html") 
@app.route("/get")
def get_bot_response():    
    question = request.args.get('msg')
    answer = chatbot.get_response(question.lower()) 

    query = False if answer.confidence > .5 else True
    if query:
    # pegar as top_words?
        lista = train_from_elasticsearch_response(question)
        #answer = chatbot.get_response(question.lower())
        return {'respostas': lista, 'isConsulta': "true"}

    return {'respostas': str(answer), 'isConsulta': "false"}

@app.route("/train")
def train_bot_with_input():
    pergunta = request.args.get('qtn')
    resposta = request.args.get('asw')
    trainer.train([pergunta, resposta])

if __name__ == "__main__":
    train_from_builtin_data(dialogos_basicos_path)     
    app.run(host='0.0.0.0', port=4040)
