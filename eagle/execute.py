import os

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

# if __name__ == '__main__':
from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (create_document_directory,
                                        create_folder, remaining_downloads)
from settings.import_list import generate_document_list
from settings.settings import web_directory
from settings.user_prompts import continue_prompt, request_more_information

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import record_document
from eagle.search import document_number_search
# else:
#     print(__name__)
#     from ..settings.abstract_object import abstract_dictionary
#     from ..settings.bad_search import record_bad_search
#     from ..settings.driver import create_webdriver
#     from ..settings.export import export_document
#     from ..settings.file_management import (create_document_directory,
#                                             create_folder, remaining_downloads)
#     from ..settings.import_list import generate_document_list
#     from ..settings.settings import web_directory
#     from ..settings.user_prompts import (continue_prompt,
#                                          request_more_information)
#     from .download import download_document
#     from .login import account_login
#     from .open_document import open_document
#     from .record import record_document
#     from .search import document_number_search


def search_documents_from_list(browser, document_list, download):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dictionary, document_number)
            if download:
                download_document(browser)
            print(f'Document located at reception number {document_number} recorded, '
                  f'{remaining_downloads(document_list, document_number)} documents remaining.')
        else:
            record_bad_search(abstract_dictionary, document_number)
            print(f'No document found at reception number {document_number}, '
                  f'{remaining_downloads(document_list, document_number)} documents remaining.')


def review_documents_from_list(browser, document_list):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            input(f'Document located at reception number {document_number} located,'
                  'please review & press enter to continue...'
                  f'({remaining_downloads(document_list, document_number)} documents remaining)')
        else:
            record_bad_search(abstract_dictionary, document_number)
            input(f'No document found at reception number {document_number}, '
                  'please review & press enter to continue...'
                  f'({remaining_downloads(document_list, document_number)} documents remaining)')


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


def execute_program(headless, target_directory, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    create_abstraction(browser, target_directory, file_name, sheet_name, download)
    while continue_prompt(target_directory, file_name, sheet_name):
        target_directory, file_name, sheet_name = \
            request_more_information(target_directory, file_name, sheet_name)
        create_abstraction(target_directory, file_name, sheet_name, download)
    browser.close()
    quit()


def execute_review(target_directory, file_name, sheet_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    review_documents_from_list(browser, document_list)
    browser.close()
    quit()


# def execute_web_program(client, legal, upload_file):
#     sheet_name = 'Documents'
#     download = False
#     file_name = upload_file
#     target_directory = web_directory
#     headless = False
#     browser = create_webdriver(target_directory, headless)
#     account_login(browser)
#     abstract_dictionary = create_abstraction(browser, target_directory, file_name, sheet_name, download)
#     browser.close()
#     return abstract_dictionary
