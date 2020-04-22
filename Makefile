# Makefile
SHELL := /bin/bash

GDRIVE_FOLDER_SHARE_ID := 1deLaPKDaWb1wGmQH5v9PTH4W1B-HZPPi
RAW_DATA_SHARE_ID := 1EQTR6Rm_0KwpkZPCqXeZg9b90ueQNZfs
SENTENCAS_RESPOSTAS_SHARE_ID := 1C_6Rvk4todyYPMzM_lrXLI4MYa4QfTiA
TOPICO_SOLICITACAO_SHARE_ID := 1-vAfoOmhPuYC-lx-HAwSnpoeEIJOptaw
METADADOS_RESPOSTAS_SHARE_ID := 1ckpytvMgbTYicnqaebw2tdkMVDIBILe0
METADADOS_DOSSIES_SHARE_ID := 1u4JFkjYEeTRhpxDGL3Z3mIcBd5L_h6uH
METADADOS_SOLICITACOES_RESPOSTAS_SHARE_ID := 1vlfv7PEX2lE8fcdVma5jt1oEgW_UgH_X

.PHONY: all env requirements fetch_data clean

all: requirements fetch_data

env:
	@echo Creating env
	@python3.7 -m venv .venv

requirements:
	@echo downloading requirements for project
	@pip install --upgrade pip
	@pip install --upgrade -r requirements.txt

before_fetch_data:
	@mkdir -p data
	@echo Fetching data

fetch_data: before_fetch_data get_raw get_metadata

get_metadata:
	@./scripts.sh gdrive_download $(SENTENCAS_RESPOSTAS_SHARE_ID) sbrt_respostas_sentencas.tsv
	@./scripts.sh move_to sbrt_respostas_sentencas.tsv data/

	@./scripts.sh gdrive_download $(TOPICO_SOLICITACAO_SHARE_ID) topico_solicitacao.yml
	@./scripts.sh move_to topico_solicitacao.yml data/

	@./scripts.sh gdrive_download $(METADADOS_RESPOSTAS_SHARE_ID) vw_respostas.xlsx
	@./scripts.sh move_to vw_respostas.xlsx data/

	@./scripts.sh gdrive_download $(METADADOS_DOSSIES_SHARE_ID) vw_dossies.xlsx
	@./scripts.sh move_to vw_dossies.xlsx data/

	@./scripts.sh gdrive_download $(METADADOS_SOLICITACOES_RESPOSTAS_SHARE_ID) sbrt_respostas_solicitacao_metadados.csv
	@./scripts.sh move_to sbrt_respostas_solicitacao_metadados.csv data/

get_raw:
	@./scripts.sh gdrive_download $(RAW_DATA_SHARE_ID) sbrt_txts.zip
	@./scripts.sh move_to sbrt_txts.zip data/preprocessed
	@unzip -d data/preprocessed data/preprocessed/sbrt_txts.zip
	@rm -rf data/preprocessed/sbrt_txts.zip

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete