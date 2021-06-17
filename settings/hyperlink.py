import os
from settings.file_management import document_directory_exists
import pandas as pd

from settings.export_settings import worksheet_properties


def remove_prefix(string, prefix):
    return string[(string.find(prefix) + 1):]


def remove_file_suffix(file_name):
    return file_name[:file_name.rfind(".")]


def strip_document_number_from_file_name(file_name):
    return remove_file_suffix(remove_prefix(file_name))


def create_hyperlinks(target_directory, hyperlink_column):
    for data in hyperlink_column:
        if data in os.listdir(document_directory):
            print("match", data)
            create_hyperlink(data)


def add_hyperlinks(target_directory, dataframe):
    if document_directory_exists(target_directory):
        hyperlink_column = dataframe[worksheet_properties["hyperlink"]]
        create_hyperlinks(target_directory, hyperlink_column)
