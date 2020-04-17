# Makefile
SHELL := /bin/bash

GDRIVE_FOLDER_SHARE_ID := 1deLaPKDaWb1wGmQH5v9PTH4W1B-HZPPi
TOPICO_SOLICITACAO_SHARE_ID := 1-vAfoOmhPuYC-lx-HAwSnpoeEIJOptaw
SENTENCAS_RESPOSTAS_SHARE_ID := 1C_6Rvk4todyYPMzM_lrXLI4MYa4QfTiA

.PHONY: all env requirements fetch_data clean

all: requirements fetch_data

env:
	@echo Creating env
	@python3 -m venv env

requirements:
	@echo downloading requirements for project
	@pip install -r requirements.txt

before_fetch_data:
	@echo Fetching data

fetch_data: before_fetch_data get_data

get_data:
	@./scripts.sh gdrive_download $(SENTENCAS_RESPOSTAS_SHARE_ID) sbrt_respostas_sentencas.tsv
	@./scripts.sh move_to sbrt_respostas_sentencas.tsv data/

	@./scripts.sh gdrive_download $(TOPICO_SOLICITACAO_SHARE_ID) topico_solicitacao.yml
	@./scripts.sh move_to topico_solicitacao.yml data/

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete