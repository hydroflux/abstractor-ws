from dataframe import abstract_dataframe
from download import download_document
from open import open_document
from record import record_bad_search, record_document
from search import document_number_search
from file_management import create_folder

import os


def create_download_directory(target_directory):
    download_directory = f'{target_directory}/Documents'
    create_folder(download_directory)
    os.chdir(download_directory)


def remaining_downloads(document_list, document_number):
    return len(document_list) - document_list.index(document_number)


def search_documents_from_list(browser, document_list, download=True):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dataframe, document_number)
            if download:
                download_document(browser)
            print(f'Document located at reception number {document_number} recorded, {remaining_downloads(document_list, document_number)} documents remaining.')
        else:
            record_bad_search(abstract_dataframe, document_number)
            print(f'No document found at reception number {document_number}, {remaining_downloads(document_list, document_number)} documents remaining.')


def execute_script(browser, target_directory, document_list, download):
    if download:
        create_download_directory(target_directory)
    search_documents_from_list(browser, document_list, download)
    return abstract_dataframe