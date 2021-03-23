import os
from pandas import DataFrame


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def create_dataframe(dictionary):
    dataframe = DataFrame(dictionary)
    print(dataframe)