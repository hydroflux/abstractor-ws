import os
import math
import pandas as pd

if __name__ == '__main__':
    from settings.settings import web_directory
    from settings.classes.Document import Document
else:
    from .settings import web_directory


def get_sheet_columns(excel_object):
    return excel_object.columns


def get_sheet_rows(excel_object):
    rows = []
    for index, row in excel_object.iterrows():
        rows.append(row)
    return rows


def is_empty_value(value):
    value_check = float(value)
    return math.isnan(value_check)


def get_book_number(row):
    book = row['Book']
    if is_empty_value(book):
        return None
    else:
        return int(book)


def import_excel_document(file_path, sheet_name):
    excel_object = pd.read_excel(file_path, sheet_name)
    int_document_list = excel_object.values.flatten().tolist()
    return [str(i) for i in int_document_list]


def generate_document_list(target_directory, file_name, sheet_name):
    file_path = f'{target_directory}/{file_name}.xlsx'
    return import_excel_document(file_path, sheet_name)


def generate_list_from_file(file_name, sheet_name):
    file_path = f'{web_directory}/{file_name}'
    return import_excel_document(file_path, sheet_name)
