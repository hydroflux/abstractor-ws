import os

from settings.classes.Hyperlink import Hyperlink
from settings.export_settings import worksheet_properties
from settings.file_management import (access_document_directory,
                                      document_directory_exists, strip_document_number_from_file_name)


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
            # Currently adding full path, may need to change to relative path after processing
            return f'/Documents/{file}'


def create_hyperlink(data, row, url):
    return Hyperlink(value=data, row=row, url=url)


def create_hyperlinks(dataframe, document_directory, hyperlink_column):
    for data in hyperlink_column:
        directory_file_numbers = get_directory_file_numbers(document_directory)
        if data in directory_file_numbers:
            row = get_data_row(dataframe, hyperlink_column, data)
            url = create_hyperlink_url(document_directory, data)
            hyperlink = create_hyperlink(data, row, url)
            hyperlink_column[row] = hyperlink
            print(data)
            print(hyperlink)
            print(hyperlink_column[row])


def add_hyperlinks(target_directory, dataframe):
    if document_directory_exists(target_directory):
        hyperlink_column = dataframe[worksheet_properties["hyperlink"]]
        document_directory = access_document_directory(target_directory)
        create_hyperlinks(dataframe, document_directory, hyperlink_column)
