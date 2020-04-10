from .paths import generated_path
import os
from os.path import join


def export_df_to_json(df, nome_do_arquivo, parent_path=None, **kwargs):
    """
    exporta o dataframe em um arquivo json

    Parameters
    ----------
    df : `pd.DataFrame`

    nome_do_arquivo : `str`
        nome final do arquivo gerado

    parent_path : `str`
        nome da pasta onde deve ser colocado o arquivo, caso seja necessario

    **kwargs:
        lista de parametros para serem passados para a função to_json do `pd.DataFrame`
    Returns
    -------
    `void`
    """
    out_path = _beforeExport(parent_path, nome_do_arquivo, 'json')
    with open(out_path, 'w', errors='replace', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False, **kwargs)


def export_df_to_csv(df, nome_do_arquivo, parent_path=None, **kwargs):
    """
    exporta o dataframe em um arquivo csv

    Parameters
    ----------
    df : `pd.DataFrame`

    nome_do_arquivo : `str`
        nome final do arquivo gerado

    parent_path : `str`
        nome da pasta onde deve ser colocado o arquivo, caso seja necessario

    **kwargs:
        lista de parametros para serem passados para a função to_csv do `pd.DataFrame`
    Returns
    -------
    `void`
    """
    out_path = _beforeExport(parent_path, nome_do_arquivo, 'csv')
    df.to_csv(out_path, **kwargs)


def _beforeExport(parent_path, nome_do_arquivo, extensao):
    if parent_path != None and not os.path.exists(join(generated_path, parent_path)):
        os.mkdir(join(generated_path, parent_path))

    out_path = join(generated_path)
    if parent_path != None:
        out_path = join(out_path, parent_path)

    return join(out_path, f'{nome_do_arquivo}.{extensao}')
