from abstract_object import abstract_dict
from download import download_document
from open import open_document
from record import record_bad_search, record_document
from search import document_number_search
from file_management import create_folder
from login import account_login
from user_prompts import continue_prompt, request_more_information
from import_list import generate_document_list
from export import export_document

import os


def create_download_directory(target_directory):
    download_directory = f'{target_directory}/Documents'
    create_folder(download_directory)
    os.chdir(download_directory)


def remaining_downloads(document_list, document_number):
    return len(document_list) - document_list.index(document_number) - 1


def search_documents_from_list(browser, document_list):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dict, document_number)
            if download:
                download_document(browser)
            print(f'Document located at reception number {document_number} recorded, \
                {remaining_downloads(document_list, document_number)} documents remaining.')
        else:
            record_bad_search(abstract_dict, document_number)
            print(f'No document found at reception number {document_number}, \
                {remaining_downloads(document_list, document_number)} documents remaining.')


def create_abstraction_dictionary(browser, target_directory, document_list, download):
    if download:
        create_download_directory(target_directory)
    search_documents_from_list(browser, document_list, download)
    return abstract_dict


def create_abstraction(browser, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract_dict = create_abstraction_dictionary(browser, target_directory, document_list, download)
    export_document(target_directory, file_name, abstract_dict)


def execute_program(browser, target_directory, file_name, sheet_name, download):
    account_login(browser)
    create_abstraction()
    while continue_prompt(target_directory, file_name, sheet_name):
        target_directory, file_name, sheet_name = \
            request_more_information(target_directory, file_name, sheet_name)
        create_abstraction(target_directory, file_name, sheet_name, download)
