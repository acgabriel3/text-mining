import yaml
import pandas as pd
import sklearn
from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.callbacks import ModelCheckpoint
from numpy import argmax
from keras.models import load_model


dados = None

with open('data/palavraschave/topico_solicitacao.yml', encoding = 'utf-8') as file:
    dados = yaml.load(file, Loader = yaml.FullLoader)

perguntas_palavras = pd.DataFrame(data = None, columns = ['sentenca', 'palavras_chave'])

#As palavras chave ainda nao estao muito boas para o contexto, pelo que vejo
for dado in dados:    
    try:
        #len(dado) - 1
        #dado = [palavra for palavra in dado if palavra not in ['serviço', 'brasileiro', 'respostas', 'técnicas', 'técnica', 'resposta']]
        palavras = " ".join(dado[1:(5)]) #para mudar qtd de top words mudar a selecao a direita
    except Exception:
        pass
    
    print(palavras)
    aux = pd.DataFrame(data = [[str(dado[0]), str(palavras)]], columns = ['sentenca', 'palavras_chave'])
    perguntas_palavras = pd.DataFrame.append(perguntas_palavras, aux, ignore_index = True) 

perguntas_palavras = perguntas_palavras.groupby(['palavras_chave']).tail(39)

def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer

def max_length(lines):
	return max(len(line.split()) for line in lines)

# codifica e coloca em tamanho unico as sentencas (o que seria um problema para as perguntas do chatbot)
def encode_sequences(tokenizer, length, lines):
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X


def encode_output(sequences, vocab_size):
	ylist = list()
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size)
		ylist.append(encoded)
	y = array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y

# define NMT model
def define_model(src_vocab, tar_vocab, src_timesteps, tar_timesteps, n_units):
	model = Sequential()
	model.add(Embedding(src_vocab, n_units, input_length=src_timesteps, mask_zero=True))
	model.add(LSTM(n_units))
	model.add(RepeatVector(tar_timesteps))
	model.add(LSTM(n_units, return_sequences=True))
	model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
	return model

# mapeia um inteiro para uma palavra conhecida pela vocabulario do tokenizador
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# Prediz as palavras chaves de uma sequencia para um determinado model
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

# Prediz todas as setencas de um dado, e monta tabela para analise dos resultados
def evaluate_model_data(model, nameModel, data, tokenizador_sentencas, tokenizador_chaves, sentencas_length):
    result_model = pd.DataFrame(data = None, columns = ['sentenca', 'palavras_chave', 'resultado'])
    
    for i, row in data.iterrows():
        print(row)
        predicted = predict_sequence(model, tokenizador_chaves, encode_sequences(tokenizador_sentencas, sentencas_length, row.sentenca))
        aux = pd.DataFrame(data = [[str(row.sentenca), str(row.palavras_chave), str(predicted)]], columns = ['sentenca', 'palavras_chave', 'resultado'])
        result_model = pd.DataFrame.append(result_model, aux, ignore_index = True)
    
    result_model.to_csv(nameModel)

#Execucao das funcoes
tokenizador_sentencas = create_tokenizer(perguntas_palavras['sentenca'])
voc_sentencas_size = len(tokenizador_sentencas.word_index) + 1
sentencas_length = max_length(perguntas_palavras['sentenca'])

tokenizador_chaves = create_tokenizer(perguntas_palavras['palavras_chave'])
voc_chaves_size = len(tokenizador_chaves.word_index) + 1
chaves_length = max_length(perguntas_palavras['palavras_chave'])


perguntas_palavras = sklearn.utils.shuffle(perguntas_palavras)
perguntas_palavras = perguntas_palavras.reset_index(drop=True)

#treinamento 90 teste 10
pos_90porcento = int((len(perguntas_palavras.sentenca) * 0.9)) - 1
train, test = perguntas_palavras[:pos_90porcento], perguntas_palavras[pos_90porcento:]

trainX = encode_sequences(tokenizador_sentencas, sentencas_length, train.sentenca)
trainY = encode_sequences(tokenizador_chaves, chaves_length, train.palavras_chave)
trainY = encode_output(trainY, voc_chaves_size)

testX = encode_sequences(tokenizador_sentencas, sentencas_length, test.sentenca)
testY = encode_sequences(tokenizador_chaves, chaves_length, test.palavras_chave)
testY = encode_output(testY, voc_chaves_size)
 
# define model
model = define_model(voc_sentencas_size, voc_chaves_size, sentencas_length, chaves_length, 256)
model.compile(optimizer='adam', loss='categorical_crossentropy')

# fit model
filename = 'model_four_tops_without_header_sbrt.h5'
checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
model.fit(trainX, trainY, epochs=1, batch_size=None, validation_data=(testX, testY), callbacks=[checkpoint], verbose=2)
































    
