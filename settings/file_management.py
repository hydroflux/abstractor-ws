import os
import shutil

from pandas import DataFrame

if __name__ == '__main__':
    from settings.settings import abstraction_type
else:
    from .settings import abstraction_type


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def create_document_directory(target_directory):
    document_directory = f'{target_directory}/Documents'
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def remaining_documents(document_list, document):
    return len(document_list) - document_list.index(document) - 1


def list_remaining_documents(document_list, document):
    return f'{remaining_documents(document_list, document)} documents remaining.'


def document_type(document):
    return str(document.type)


def document_value(document):
    if document_type(document) == "document_number":
        return str(document.value)
    elif document_type(document) == "book_and_page":
        return [str(document.value["Book"]), str(document.value["Page"])]


def extrapolate_document_value(document):
    value = document_value(document)
    if type(value) == list:
        return f'Book: {value[0]}, Page: {value[1]}'
    elif type(value) == str:
        return f'number {value}'


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


def bundle_project(target_directory, file_name):
    os.chdir(target_directory)
    project_folder = f'{target_directory}/{file_name}'
    create_folder(project_folder)
    shutil.move(f'{target_directory}/Documents', project_folder)
    # shutil.move(f'{target_directory}/{file_name}.xlsx', project_folder)
    shutil.move(f'{target_directory}/{file_name}-{abstraction_type.upper()}.xlsx', project_folder)
