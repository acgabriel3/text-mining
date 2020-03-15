from pathlib import Path
import os


this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
data_dir = this_file_dir / '..' / '..' / 'data'

dossies_path = data_dir / 'raw' / 'dossies'
respostas_path = data_dir / 'raw' / 'respostas'

dossies_metadados_path = data_dir / 'processed' / 'dossies_metadados.json'
respostas_metadados_path = data_dir / 'processed' / 'respostas_metadados.json'
vocabulario_controlado_path = data_dir / \
    'processed' / 'vocabulario_controlado.html'
