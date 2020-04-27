import math
import json
import logging
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from elasticsearch import Elasticsearch

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
                    "query": f'{q} {top_words}'
                }
            }
        }
    })

    if _DEV:
        print([hit['_source']['sentenca'] for hit in res['hits']['hits']])

    for hit in res['hits']['hits']:
        if len(hit['_source']['sentenca'].split()) > 1:
            trainer.train([q, hit['_source']['sentenca']])

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
        train_from_elasticsearch_response(question)
        answer = chatbot.get_response(question.lower())

    return str(answer) 

if __name__ == "__main__":
    train_from_builtin_data()     
    app.run(host='0.0.0.0', port=4040)
