from pathlib import Path
import os


_this_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
_data_dir = _this_file_dir / '..' / '..' / 'data'

pre_processed_respostas_dir = _data_dir / \
    'preprocessed' / 'sbrt_txts' / 'respostas_txt'
respostas_lematizadas_dir = _data_dir / 'preprocessed' / \
    'sbrt_txts' / 'respostas_lematizadas'

topicos_solicitacao_path = _data_dir / 'topico_solicitacao.yml'
sentencas_respostas_path = _data_dir / 'sbrt_respostas_sentencas.tsv'
vw_dossies_path = _data_dir / 'vw_dossies.xlsx'
vw_respostas_path = _data_dir / 'vw_respostas.xlsx'
solicitacoes_path = _data_dir / 'sbrt_respostas_solicitacao_metadados.csv'
