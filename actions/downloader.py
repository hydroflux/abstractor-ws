import os

from settings.initialization import create_folder


def create_document_directory(target_directory):
    document_directory = f'{target_directory}/Documents'
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def prepare_for_download(abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))
    if abstract.county.engine == 'jaguar':
        document.download_value = f'{document.reception_number}.pdf'