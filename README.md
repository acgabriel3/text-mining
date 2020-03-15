sbrt_ibict_ml
==============================

Aprimoramento da recuperação de informação para o site http://sbrt.ibict.br/

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


Objetivos deste projeto
------------

- ### Produto 4

    #### Avaliação de metodologias para extração semi-automática de taxonomia:

    - [ ] Avaliação de métodos para a extração de termos (estatístico, linguístico, híbrido etc.);
    - [ ] Realização extração de termos no Banco de Respostas para desenvolvimento de protótipo;
    - [ ] Identificação relações conceituais ou mapas conceituais;
    - [ ] Organização hierárquica dos termos extraídos;
    - [ ] Elaboração de taxonomia gerada a partir de extração semiautomática;
    - [ ] Identificação dos benefícios da utilização da técnica de extração semiautomática de taxonomia;
    - [ ] Identificação das melhores técnicas de agrupamentos;
    - [ ] Apresentação proposta de atualização e manutenção da taxonomia do SBRT em modelo híbrido.

    #### Resultados esperados

    - Avaliação o método adequado para a extração de termos (estatístico, linguístico, híbrido etc.) no Banco de Respostas;
    - Realização extração de termos no Banco de Respostas para desenvolvimento de protótipo;
    - Identificação relações conceituais ou mapas conceituais entre as respostas técnicas, respostas referenciais e dossiês;
    - Organização hierárquica dos termos extraídos para apresentar protótipo de taxonomia gerada a partir de extração semiautomática;
    - Identificação os benefícios da utilização da técnica de extração semiautomática no contexto do SBRT;
    - Identificação das melhores técnicas de agrupamentos de documentos no âmbito do SBRT.

- ### Produto 5

    #### Avaliação de técnicas de mineração de texto para descoberta de conhecimento e identificação de padrões:

    - [ ] Avaliação dos algoritmos de mineração de texto e sugestão para uso no SBRT;
    - [ ] Construção de base textual para prototipagem de mineração de textos (ETL, mineração, descobrimento de padrões);
    - [ ] Identificação de preocupações ocultas, tendências de mercado, sequenciamento de soluções tecnológicas;
    - [ ] Elaboração de diretrizes para a utilização de técnicas de text mining para descoberta de conhecimento e identificação de padrões no banco de respostas do SBRT;
    - [ ] Verificação da aplicabilidade do uso de chatbot e definição de fluxo da aplicação;
    - [ ] Identificação da possibilidade de aplicação da tecnologia de machine learning na base da pirâmide informacional do SBRT.


    #### Resultados esperados

    - Avaliação dos algoritmos de mineração de texto, pontos fortes e fracos para utilização no SBRT;
    - Sugestão de algoritmo de mineração de texto adequado a extração de conhecimentos e realização de predições no banco de dados do SBRT (RT, RR e Dossiês).

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
