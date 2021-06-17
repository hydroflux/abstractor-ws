import os
from settings.classes.Hyperlink import Hyperlink
from settings.file_management import access_document_directory, document_directory_exists

from settings.export_settings import worksheet_properties


def remove_prefix(string, prefix):
    return string[(string.find(prefix) + 1):]


def remove_file_suffix(file_name):
    return file_name[:file_name.rfind(".")]


def strip_document_number_from_file_name(file_name):
    return remove_file_suffix(remove_prefix(file_name, "-"))


def get_directory_files(directory):
    return os.listdir(directory)


def get_directory_file_numbers(document_directory):
    return list(map(strip_document_number_from_file_name, get_directory_files(document_directory)))


def get_data_row(dataframe, column, data):
    return dataframe.index[column == data]


def create_hyperlink_url(document_directory, data):
    directory_files = get_directory_files(document_directory)
    for file in directory_files:
        if strip_document_number_from_file_name(file) == data:
            print(f'{document_directory}/{file}')
            return f'{document_directory}/{file}'


def create_hyperlink(data, row, url):
    return Hyperlink(value=data, row=row, url=url)


def create_hyperlinks(dataframe, document_directory, hyperlink_column):
    for data in hyperlink_column:
        directory_file_numbers = get_directory_file_numbers(document_directory)
        if data in directory_file_numbers:
            row = get_data_row(dataframe, hyperlink_column, data)
            url = create_hyperlink_url()
            hyperlink = create_hyperlink(data, row, url)
            print(hyperlink)


def add_hyperlinks(target_directory, dataframe):
    if document_directory_exists(target_directory):
        hyperlink_column = dataframe[worksheet_properties["hyperlink"]]
        document_directory = access_document_directory(target_directory)
        create_hyperlinks(document_directory, hyperlink_column)
