from pathlib import Path
import os


_this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
_data_dir = _this_file_dir / '..' / '..' / 'data'
_reports_dir = _this_file_dir / '..' / '..' / 'reports'

figures_path = _reports_dir / 'figures'

raw_dossies_path = _data_dir / 'raw' / 'sbrt_txts' / 'dossies'
raw_respostas_path = _data_dir / 'raw' / 'sbrt_txts' / 'respostas'

interim_dossies_path = _data_dir / 'preprocessed' / 'dossies'
interim_respostas_path = _data_dir / 'preprocessed' / 'respostas'

dossies_metadados_path = _data_dir / 'processed' / 'dossies_metadados.json'
respostas_metadados_path = _data_dir / 'processed' / 'respostas_metadados.json'
vocabulario_controlado_path = _data_dir / \
    'processed' / 'voc_controlado.xlsx'
