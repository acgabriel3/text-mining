import math
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

logging.basicConfig(level=logging.INFO)

data = json.loads(open('dialogo.json', 'r').read())

train = []
tag = []

for row in data:
    train.append(row['question'])
    train.append(row['answer'])

for row in data:
    tag.append(row['flag'])

chatbot = ChatBot('Sara')

trainer = ListTrainer(chatbot)
trainer.train(train)

while True: 
    try:
        question = input('Usuário: ')
        answer = chatbot.get_response(question.lower())
        txt = str(answer)
        
        idx = math.floor(train.index(txt) / 2)

        query = False
        for i, val in enumerate(tag):
            if val == 'consulta': 
                query = True
                break
            if i == idx: break

        if query == True:
            print('Consulta')                               ##### Conectar ao elasticsearch ##### 
        else:
           print(f'{chatbot.name}: {answer}')
    
    except(KeyboardInterrupt, EOFError, SystemExit):
        break

