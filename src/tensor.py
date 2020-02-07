from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow import keras, nn
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('webAgg')  # abre um navegador pra visualizar o gráfico gerado

# totalmente baseado em: https://www.tensorflow.org/tutorials/keras/text_classification


def plotGrafico(history):
    history_dict = history.history
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    epochs = range(1, len(acc) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(epochs, acc, 'bo-', label='Training accuracy')
    ax1.plot(epochs, val_acc, 'r', label='Validation accuracy')
    ax1.set(
        xlabel='Epochs',
        ylabel='Accuracy',
        title='Training and validation accuracy'
    )
    ax1.grid()
    ax1.legend()

    ax2.plot(epochs, loss, 'bo', label='Training loss')
    ax2.plot(epochs, val_loss, 'r', label='Validation loss')
    ax2.set(
        xlabel='Epochs',
        ylabel='Loss',
        title='Training and validation loss'
    )
    ax2.grid()
    ax2.legend()

    fig.savefig("nn.png")
    plt.show()

# retorna a string decodificada


def decode_review(word_index, text):
    reverse_word_index = dict(
        [(value, key) for (key, value) in word_index.items()]
    )
    return ' '.join([reverse_word_index.get(i, "?") for i in text])

# função que adiciona 0's ao final das strings para que todas tenham o mesmo tamanho


def padStringsOf(data, maxlen):
    return keras.preprocessing.sequence.pad_sequences(
        data,
        value=word_index["<PAD>"],
        padding="post",
        maxlen=maxlen
    )


if __name__ == "__main__":
    imdb = keras.datasets.imdb
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

    word_index = imdb.get_word_index()
    # shifta os valores em 3 para poder adicionar novas labels
    word_index = {
        k: (v+3) for k, v in word_index.items()
    }
    word_index["<PAD>"] = 0
    word_index["<START>"] = 1
    word_index["<UNK>"] = 2
    word_index["<UNUSED>"] = 3

    # As avaliações dos filmes têm diferentes tamanhos. Sabendo que o número
    # de entradas da rede neural tem que ser de mesmo tamanho, então faz-se
    # necessário adicionar valores ao fim da string a fim de igualá-las
    x_train = padStringsOf(x_train, 256)
    x_test = padStringsOf(x_test, 256)

    vocab_size = 10000

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=nn.relu))
    model.add(keras.layers.Dense(1, activation=nn.sigmoid))

    # resumo do modelo criado
    model.summary()

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    x_val = x_train[:vocab_size]
    partial_x_train = x_train[vocab_size:]

    y_val = y_train[:vocab_size]
    partial_y_train = y_train[vocab_size:]

    history = model.fit(
        partial_x_train,
        partial_y_train,
        epochs=40,
        batch_size=512,
        validation_data=(x_val, y_val),
        verbose=2
    )

    results = model.evaluate(x_test, y_test)
    print(results)

    # plotGrafico(history)
