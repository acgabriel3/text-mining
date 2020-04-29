# Makefile
SHELL := /bin/bash

GDRIVE_FOLDER_SHARE_ID := 19pkZi3rZbtUxVEFq7L-ttE6sZTX9zTN1
RAW_DATA_SHARE_ID := 1RzaoH_cFHC_S0hYm5QzD2OO892rvCSP6
DOSSIES_METADADOS_SHARE_ID := 1EJ3nBF7Cqe8N46nu8-ysS5PSl0Emz1yC
RESPOSTAS_METADADOS_SHARE_ID := 10iHcTuHPcudqYeLLtwxk3bqnjn3B3u-a
VOC_CONTROLADO_SHARE_ID := 1AOher12JPOHseEVop6cc0PDam2L3px2u

.PHONY: all env requirements fetch_data preprocess_data clean

all: requirements fetch_data

env:
	@echo Creating env
	@python3 -m venv .venv

requirements:
	@echo downloading requirements for project
	@pip install --upgrade pip
	@pip install --upgrade -r requirements.txt

before_fetch_data:
	@echo Fetching data
	@chmod +x ./scripts.sh

fetch_data: before_fetch_data get_raw get_metadata

preprocess_data: requirements
	@mkdir -p data/preprocessed
	@python3 src/data/preprocess.py --src=$$SRC

get_metadata:
	@./scripts.sh gdrive_download $(RESPOSTAS_METADADOS_SHARE_ID) respostas_metadados.json
	@./scripts.sh move_to respostas_metadados.json data/processed

	@./scripts.sh gdrive_download $(DOSSIES_METADADOS_SHARE_ID) dossies_metadados.json
	@./scripts.sh move_to dossies_metadados.json data/processed

	@./scripts.sh gdrive_download $(VOC_CONTROLADO_SHARE_ID) voc_controlado.xlsx
	@./scripts.sh move_to voc_controlado.xlsx data/processed

get_raw:
	@./scripts.sh gdrive_download $(RAW_DATA_SHARE_ID) sbrt_raw.zip
	@./scripts.sh move_to sbrt_raw.zip data/raw
	@unzip -P "segredo" -d data/raw data/raw/sbrt_raw.zip
	@rm -rf data/raw/sbrt_raw.zip

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete