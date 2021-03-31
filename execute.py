import os

from .abstract_object import abstract_dictionary
from .download import download_document
from .driver import chrome_webdriver
from .export import export_document
from .file_management import create_folder
from .import_list import generate_document_list
from .login import account_login
from .open import open_document
from .record import record_document
from .search import document_number_search
from .bad_search import record_bad_search
from .user_prompts import continue_prompt, request_more_information
from .file_management import create_document_directory, remaining_downloads

from .variables import web_directory


def search_documents_from_list(browser, document_list, download):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dictionary, document_number)
            if download:
                download_document(browser)
            print(f'Document located at reception number {document_number} recorded, {remaining_downloads(document_list, document_number)} documents remaining.')
        else:
            record_bad_search(abstract_dictionary, document_number)
            print(f'No document found at reception number {document_number}, {remaining_downloads(document_list, document_number)} documents remaining.')


def create_abstraction_dictionary(browser, target_directory, document_list, download):
    if download:
        create_document_directory(target_directory)
    search_documents_from_list(browser, document_list, download)
    return abstract_dictionary


def create_abstraction(browser, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract_dictionary = create_abstraction_dictionary(browser, target_directory, document_list, download)
    export_document(target_directory, file_name, abstract_dictionary)
    return abstract_dictionary


def execute_program(target_directory, file_name, sheet_name, download):
    browser = chrome_webdriver(target_directory)
    account_login(browser)
    create_abstraction(browser, target_directory, file_name, sheet_name, download)
    while continue_prompt(target_directory, file_name, sheet_name):
        target_directory, file_name, sheet_name = \
            request_more_information(target_directory, file_name, sheet_name)
        create_abstraction(target_directory, file_name, sheet_name, download)
    browser.close()
    quit()


def execute_web_program(client, legal, upload_file):
    sheet_name = 'Documents'
    download = False
    file_name = upload_file
    target_directory = web_directory
    browser = chrome_webdriver(target_directory)
    account_login(browser)
    abstract_dictionary = create_abstraction(browser, target_directory, file_name, sheet_name, download)
    browser.close()
    return abstract_dictionary
