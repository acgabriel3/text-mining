#funcoes auxiliares para ambos os pacotes (antes do pre-processamento)

import pandas as pd


def contadorPalavras(string): 
    words = string.split()
    return len(words)

def tamanho_medio_palavras(string):  
    words = string.split()
    tamanhoPalavras = [len(word) for word in words]
    
    media = sum(tamanhoPalavras)/len(words)
    return media

#Interessante para buscas no texto
def contador_palavras_termo(string, termo):
    words = string.split()
    termos = [word for word in words if word.startswith(termo)]
    
    return len(termos)

soma = 0
for i in list(range(1, len(dossies['texto']), 1)):
    numeroPalavras = contadorPalavras(str(dossies['texto'][i]))
    soma = soma + numeroPalavras
    print(numeroPalavras)

for i in list(range(1, len(dossies['texto']), 1)):
    mediaPalavras = tamanho_medio_palavras(str(dossies['texto'][i]))
    print(mediaPalavras)
