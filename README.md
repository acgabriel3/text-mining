# Produto 5

## Avaliação de técnicas de mineração de texto para descoberta de conhecimento e identificação de padrões:

- [ ] Avaliação dos algoritmos de mineração de texto e sugestão para uso no SBRT;
- [ ] Construção de base textual para prototipagem de mineração de textos (ETL, mineração, descobrimento de padrões);
- [ ] Identificação de preocupações ocultas, tendências de mercado, sequenciamento de soluções tecnológicas;
- [ ] Elaboração de diretrizes para a utilização de técnicas de text mining para descoberta de conhecimento e identificação de padrões no banco de respostas do SBRT;
- [ ] Verificação da aplicabilidade do uso de chatbot e definição de fluxo da aplicação;
- [ ] Identificação da possibilidade de aplicação da tecnologia de machine learning na base da pirâmide informacional do SBRT.


## Resultados esperados

- Avaliação dos algoritmos de mineração de texto, pontos fortes e fracos para utilização no SBRT;
- Sugestão de algoritmo de mineração de texto adequado a extração de conhecimentos e realização de predições no banco de dados do SBRT (RT, RR e Dossiês).

## Como executar

#### Instale as seguintes dependencias no Linux

```
$ sudo apt install python3-venv python3-dev unzip
```

Em um terminal unix execute para baixar os dados necessários:

```
$ make env
$ source env/bin/activate
$ make
```

#### Para rodar o chatbot execute:

```
$ (text-mining) python3 src/main.py
```

#### Removendo o env criado:

```
$ deactivate
$ rm -rf env
```
