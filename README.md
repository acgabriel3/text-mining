# Produto 4

## Avaliação de metodologias para extração semiautomática de taxonomia:

- [ ] Avaliação de métodos para a extração de termos (estatístico, linguístico, híbrido etc.);
- [ ] Realização extração de termos no Banco de Respostas para desenvolvimento de protótipo;
- [ ] Identificação relações conceituais ou mapas conceituais;
- [ ] Organização hierárquica dos termos extraídos;
- [ ] Elaboração de taxonomia gerada a partir de extração semiautomática;
- [ ] Identificação dos benefícios da utilização da técnica de extração semiautomática de taxonomia;
- [ ] Identificação das melhores técnicas de agrupamentos;
- [ ] Apresentação proposta de atualização e manutenção da taxonomia do SBRT em modelo híbrido.

## Resultados esperados

- Avaliação o método adequado para a extração de termos (estatístico, linguístico, híbrido etc.) no Banco de Respostas;
- Realização extração de termos no Banco de Respostas para desenvolvimento de protótipo;
- Identificação relações conceituais ou mapas conceituais entre as respostas técnicas, respostas referenciais e dossiês;
- Organização hierárquica dos termos extraídos para apresentar protótipo de taxonomia gerada a partir de extração semiautomática;
- Identificação os benefícios da utilização da técnica de extração semiautomática no contexto do SBRT;
- Identificação das melhores técnicas de agrupamentos de documentos no âmbito do SBRT.

## Como executar

Instale as seguintes dependencias no Linux

```
$ sudo apt install python3-venv unzip
```

Em um terminal unix execute para baixar os dados necessários:

```
$ make env
$ source env/bin/activate
$ make
```

Para criar os arquivos pre-processados execute:

```
$ make preprocess_data SRC=dossies
$ make preprocess_data SRC=respostas
```
