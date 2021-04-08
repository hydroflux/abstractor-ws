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


def get_page_number(row):
    page = row['Page']
    if is_empty_value(page):
        return None
    else:
        return int(page)


def get_document_number(row):
    document_number = row['Document']
    if is_empty_value(document_number):
        return None
    else:
        return int(document_number)


def store_document(document_list, type, value):
    document = Document(type=type, value=value)
    document_list.append(document)


def create_book_and_page_object(document_list, row):
    book = get_book_number(row)
    page = get_page_number(row)
    if book is not None and page is not None:
        book_and_page = {
            "Book": book,
            "Page": page
        }
        store_document(document_list, "book_and_page", book_and_page)


def create_document_number_object(document_list, row):
    document_number = get_document_number(row)
    if document_number is not None:
        store_document(document_list, "document_number", document_number)


def create_document_list(excel_object):
    document_list = []
    columns = get_sheet_columns(excel_object)
    rows = get_sheet_rows(excel_object)
    for row in rows:
        if 'Book' in columns and 'Page' in columns:
            create_book_and_page_object(document_list, row)
        if 'Document' in columns or 'Documents' in columns or \
                                    'Reception Number' in columns or \
                                    'Reception Numbers' in columns:
            create_document_number_object(document_list, row)
    return document_list


def import_excel_document(file_path, sheet_name):
    excel_object = pd.read_excel(file_path, sheet_name)
    return create_document_list(excel_object)


def generate_document_list(target_directory, file_name, sheet_name):
    file_path = f'{target_directory}/{file_name}.xlsx'
    return import_excel_document(file_path, sheet_name)


def generate_list_from_file(file_name, sheet_name):
    file_path = f'{web_directory}/{file_name}'
    return import_excel_document(file_path, sheet_name)
