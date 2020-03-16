from src.data.make_metadados import termos_vocab
from src.data.paths import (
    raw_dossies_path,
    raw_respostas_path,
    interim_dossies_path,
    interim_respostas_path
)
from os import listdir
from os.path import isfile, join
import numpy as np
import string
import re
import nltk
import click
import os


def _load_files(path, seed=None):
    files = np.array([f for f in listdir(path)
                      if isfile(join(path, f))])
    if seed is not None:
        np.random.seed(seed)
        np.random.shuffle(files)
    return files


# se o nltk der problema para rodar descomente essa parte
def _download_nltk_dependencies():
    nltk.download('stopwords')
    nltk.download('rslp')
    nltk.download('rslp')


def basic_pre_process(text):
    """
    realiza um pré processamento básico nos textos.

    Retirada de palavras inúteis que se repetem muito, pontuação, espaçamentos
    e números

    Parameters
    ----------
    text : `str`
        texto o qual será pré-processado

    Returns
    -------
    `str`:
        string sem pontuação e apenas com as palavras que estão no vocabulário controlado
    """
    text = re.sub(
        r'Copyright . Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br', '', text)
    text = re.sub(r'dossiê técnico', '', text)
    text = re.sub(r'd o s si ê t é c n i c o', '', text)

    # remove pontuação da forma mais eficiente possivel
    text = text.translate(str.maketrans(' ', ' ', string.punctuation)).lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)

    tokens = nltk.word_tokenize(text, language='portuguese')

    no_stop_word_tokens = [
        word for word in tokens if word not in [
            nltk.corpus.stopwords.words('portuguese'),
            'copyright', '©', 'sbrt', 'ibict', 'httpwwwsbrtibictbr', "˙˘˙"
        ]
    ]

    return " ".join(
        [word for word in no_stop_word_tokens if word in termos_vocab]
    )


@click.command()
@click.option('--data',
              type=click.Choice(['dossies', 'respostas']),
              #   case_sensitive=False,
              help='data to be preprocessed')
def main(data):
    """
    Pré-processa os documentos e salva o resultado intermediário.

    Executa a função `basic_pre_process` no texto de cada documento, e então,
    salva o intermediário na pasta
    data/interim/[dossies | respostas]/arquivo_processado.txt

    Parameters
    ----------
    data : `str`
        string que representa se é para ser pré-processado os dossiês ou as
        respostas
    """
    data_path, out_path = (raw_respostas_path, interim_respostas_path) if data == 'respostas' else (
        raw_dossies_path, interim_dossies_path)

    arquivos = _load_files(data_path)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for file in arquivos:
        # necessário setar o enconding pra conseguir ler de forma correta os caracteres
        print('pre processing', file)
        doc = open(join(data_path, file),
                   errors='replace', encoding='cp1252')
        # remove pontuação da forma mais eficiente possivel
        text = basic_pre_process(" ".join(doc.readlines()))

        out_doc = open(join(out_path, file), mode='w', encoding='cp1252')
        out_doc.write(text)


if __name__ == "__main__":
    main()
