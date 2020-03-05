from pathlib import Path
import os

this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))

data_dir = Path(this_file_dir / '..' / '..' / 'data' / 'sbrt_txts')
dossies_path = data_dir / 'dossies'
respostas_path = data_dir / 'respostas'
