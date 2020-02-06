from tensorflow import keras
import numpy as np


if __name__ == "__main__":
    data = keras.models.load_model('imdb')
    print(data)