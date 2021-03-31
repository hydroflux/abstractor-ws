import os

import pandas as pd

if __name__ == '__main__':
    from settings.settings import web_directory
else:
    from .settings.settings import web_directory


def import_excel_document(file_path, sheet_name):
    excel = pd.read_excel(file_path, sheet_name)
    int_document_list = excel.values.flatten().tolist()
    return [str(i) for i in int_document_list]


def generate_document_list(target_directory, file_name, sheet_name):
    file_path = f'{target_directory}/{file_name}.xlsx'
    return import_excel_document(file_path, sheet_name)


def generate_list_from_file(file_name, sheet_name):
    file_path = f'{web_directory}/{file_name}'
    return import_excel_document(file_path, sheet_name)
