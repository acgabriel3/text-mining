from pathlib import Path
import os


_this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
_data_dir = _this_file_dir / '..' / '..' / 'data'

raw_dossies_path = _data_dir / 'raw' / 'dossies'
raw_respostas_path = _data_dir / 'raw' / 'respostas'

interim_dossies_path = _data_dir / 'interim' / 'dossies'
interim_respostas_path = _data_dir / 'interim' / 'respostas'

dossies_metadados_path = _data_dir / 'processed' / 'dossies_metadados.json'
respostas_metadados_path = _data_dir / 'processed' / 'respostas_metadados.json'
vocabulario_controlado_path = _data_dir / \
    'processed' / 'vocabulario_controlado_geral.xlsx'
