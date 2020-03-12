from pathlib import Path
import os

this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))

data_dir = Path(this_file_dir / '..' / '..' / 'data')
sbrt_txts = data_dir / 'sbrt_txts'
dossies_path = sbrt_txts / 'dossies'
respostas_path = sbrt_txts / 'respostas'

dossies_metadados_path = data_dir / 'dossies_metadados.json'
respostas_metadados_path = data_dir / 'respostas_metadados.json'
vocabulario_controlado_path = data_dir / 'sbrt_vocabulario.txt'