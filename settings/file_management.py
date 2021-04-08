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


def remaining_downloads(document_list, document_number):
    return len(document_list) - document_list.index(document_number) - 1


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
