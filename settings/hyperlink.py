import os
import pandas as pd


def remove_prefix(string, prefix):
    return string[(string.find(prefix) + 1):]


def remove_file_suffix(file_name):
    return file_name[:file_name.rfind(".")]


def strip_document_number_from_file(number):
    return 


def add_hyperlinks(dataframe, target_directory):
    hyperlink_column = dataframe[worksheet_properties["hyperlink"]]
    print("hyperlink_column", hyperlink_column, "type", type(hyperlink_column))
    for data in hyperlink_column:
        if data in os.listdir(document_directory):
            print("match", data)
            create_hyperlink(data)


def add_hyperlinks(data):
    pass