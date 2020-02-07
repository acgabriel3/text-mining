from glob import glob
import numpy as np
import os
import re
import string
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

# totalmente baseado em: https://gdcoder.com/sentiment-clas/


def load_texts_labels_from_folders(path, folders):
    texts, labels = [], []
    for idx, label in enumerate(folders):
        for fname in glob(os.path.join(path, label, '*.*')):
            texts.append(open(fname, 'r').read())
            labels.append(idx)
    # stored as np.int8 to save space
    return texts, np.array(labels).astype(np.int8)


if __name__ == "__main__":
    PATH = 'dados/aclImdb'
    names = ['neg', 'pos']
    trn, trn_y = load_texts_labels_from_folders(f'{PATH}/train', names)
    val, val_y = load_texts_labels_from_folders(f'{PATH}/test', names)

    # tamanho dos conjuntos
    # print(len(val), len(trn_y), len(val), len(val_y))
    # metade esta rotulado como 1, ou seja, é balanceado
    # print(len(trn_y[trn_y == 1]), len(val_y[val_y == 1]))

    # print(f'Classes: {np.unique(trn_y)}')
    # print(trn[0])
    # print()
    # print(f"Review's label: {trn_y[0]}")
    def tokenize(s):
        re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
        return re_tok.sub(r' \1 ', s).split()

    # create term documetn matrix
    veczr = CountVectorizer(tokenizer=tokenize, min_df=5, ngram_range=(1, 3))
    trn_term_doc = veczr.fit_transform(trn)
    # Important: Use same vocab for validation set
    val_term_doc = veczr.transform(val)

    w0 = set([o.lower() for o in trn[5].split(' ')])
    vocab = veczr.get_feature_names()
