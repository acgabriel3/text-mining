from .make_metadados import termos_vocab
import string
import re
import nltk


# se o nltk der problema para rodar descomente essa parte
# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('rslp')


def basic_pre_process(text):
    # remove pontuação da forma mais eficiente possivel
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    text = re.sub(r'serviço brasileiro de respostas técnicas', '', text)
    text = re.sub(r'dossiê técnico', '', text)
    text = re.sub(r'd o s si ê t é c n i c o', '', text)

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
