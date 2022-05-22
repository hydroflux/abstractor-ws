import os
from settings.download_management import previously_downloaded, update_download

from settings.initialization import create_folder


def create_document_directory(target_directory):
    document_directory = f'{target_directory}/Documents'
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def prepare_for_download(abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))


def download_document(browser, abstract, document, execute_download, update=True):
    prepare_for_download(abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
        if update:
            update_download(browser, abstract, document)
