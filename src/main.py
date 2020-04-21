from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot('Bot')

# Start by training our bot with the ChatterBot corpus data
trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.portuguese')

while True:
    try:
        response = chatbot.get_response(input('Usuário: '))
        print(f'{chatbot.name}: {response}')
    except:
        break
