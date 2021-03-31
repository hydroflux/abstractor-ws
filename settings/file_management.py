import os

from pandas import DataFrame


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def create_document_directory(target_directory):
    document_directory = create_folder(f'{target_directory}/Documents')
    os.chdir(document_directory)
    return document_directory


def remaining_downloads(document_list, document_number):
    return len(document_list) - document_list.index(document_number) - 1


def create_dataframe(dictionary):
    dataframe = DataFrame(dictionary)
    print(dataframe)


def rename_documents_in_directory(county, directory):
    os.chdir(directory)
    for pdf in os.listdir(directory):
        if pdf == '.DS_Store':
            full_path = os.path.join(directory, pdf)
            os.remove(full_path)
        elif pdf.startswith(county.prefix):
            continue
        else:
            new_document_name = county.prefix + '-' + pdf
            full_path = os.path.join(directory, pdf)
            os.rename(full_path, new_document_name)
            size = os.stat(new_document_name) == 0
            if size is True:
                os.remove(new_document_name)
                print('Failed to download reception number ' + pdf)
