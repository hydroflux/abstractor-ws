import math

import pandas as pd

from settings.classes.Document import Document

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("import_list", __name__)


def get_sheet_columns(excel_object):
    return excel_object.columns


def get_sheet_rows(excel_object):
    rows = []
    for index, row in excel_object.iterrows():
        rows.append(row)
    return rows


def is_missing(value):
    if pd.isnull(value):
        return True


def is_empty_value(value):
    try:
        value_check = float(value)
        return math.isnan(value_check)
    except ValueError:
        return False


def get_book_number(row):
    book = row['Book']
    if is_missing(book) or is_empty_value(book):
        return None
    else:
        try:
            return int(book)
        except ValueError:
            return str(book).strip()


def get_volume_number(row):
    volume = row['Volume']
    if is_missing(volume) or is_empty_value(volume):
        return None
    else:
        try:
            return int(volume)
        except ValueError:
            return str(volume).strip()


def get_page_number(row):
    page = row['Page']
    if is_missing(page) or is_empty_value(page):
        return None
    else:
        try:
            return int(page)
        except ValueError:
            return str(page).strip()


def get_document_number(columns, row):
    if 'Document' in columns:
        document_number = row['Document']
    elif 'Documents' in columns:
        document_number = row['Documents']
    elif 'Reception Number' in columns:
        document_number = row['Reception Number']
    elif 'Reception Numbers' in columns:
        document_number = row['Reception Numbers']
    if is_missing(document_number) or is_empty_value(document_number):
        return None
    else:
        try:
            return str(int(document_number)).strip()
        except ValueError:
            return str(document_number).strip()


def get_year(columns, row):
    if 'Recording Date' in columns:
        year = row['Recording Date']
    elif 'Recording Dates' in columns:
        year = row['Recording Dates'][-4:]
    if year:
        try:
            return year[-4:]
        except TypeError:
            return year.year
        except AttributeError:
            return None
    else:
        return None


def store_document(document_list, type, value, year):
    if year is None:
        document = Document(type=type, value=value)
    else:
        document = Document(type=type, value=value, year=year)
    document_list.append(document)


def create_book_and_page_object(document_list, row, year):
    book = get_book_number(row)
    page = get_page_number(row)
    if book is not None and page is not None:
        book_and_page = {
            "Book": book,
            "Page": page
        }
        store_document(document_list, "book_and_page", book_and_page, year)


def create_volume_and_page_object(document_list, row, year):
    volume = get_volume_number(row)
    page = get_page_number(row)
    if volume is not None and page is not None:
        volume_and_page = {
            "Volume": volume,
            "Page": page
        }
        store_document(document_list, "volume_and_page", volume_and_page, year)


def create_document_number_object(document_list, columns, row, year):
    document_number = get_document_number(columns, row)
    if document_number is not None:
        store_document(document_list, "document_number", document_number, year)


def build_book_volume_page_into_list(document_list, columns, row, year):
    if 'Book' in columns and 'Page' in columns:
        create_book_and_page_object(document_list, row, year)
    if 'Volume' in columns and 'Page' in columns:
        create_volume_and_page_object(document_list, row, year)


def build_document_number_into_list(document_list, columns, row, year):
    if 'Document' in columns or 'Documents' in columns or \
                                'Reception Number' in columns or \
                                'Reception Numbers' in columns:
        create_document_number_object(document_list, columns, row, year)


def create_document_list(excel_object):
    document_list = []
    columns = get_sheet_columns(excel_object)
    rows = get_sheet_rows(excel_object)
    for row in rows:
        year = get_year(columns, row)
        build_book_volume_page_into_list(document_list, columns, row, year)
        build_document_number_into_list(document_list, columns, row, year)
        # if 'Book' in columns and 'Page' in columns:
        #     create_book_and_page_object(document_list, row)
        # if 'Volume' in columns and 'Page' in columns:
        #     create_volume_and_page_object(document_list, row)
        # if 'Document' in columns or 'Documents' in columns or \
        #                             'Reception Number' in columns or \
        #                             'Reception Numbers' in columns:
        #     create_document_number_object(document_list, columns, row)
    return document_list


def import_excel_document(file_path, sheet_name):
    excel_object = pd.read_excel(file_path, sheet_name)
    return create_document_list(excel_object)


def generate_document_list(target_directory, file_name, sheet_name):
    file_path = f'{target_directory}/{file_name}.xlsx'
    return import_excel_document(file_path, sheet_name)


# def generate_list_from_file(file_name, sheet_name):
#     file_path = f'{web_directory}/{file_name}'
#     return import_excel_document(file_path, sheet_name)
