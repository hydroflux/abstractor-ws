import os

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import remaining_documents, document_value
from settings.import_list import generate_document_list
from settings.settings import web_directory
from settings.user_prompts import continue_prompt, request_more_information

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import record_document
from eagle.search import document_search


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document in document_list:
        if open_document(browser, document):
            record_document(browser, abstract_dictionary, document)
            if download:
                download_document(browser, target_directory, county, document)
            print(f'Document located at {str(document.value)} recorded, '
                  f'{remaining_documents(document_list, document)}')
        else:
            record_bad_search(abstract_dictionary, document)
            print(f'No document found at {str(document.value)}, '
                  f'{remaining_documents(document_list, document)}')
    return abstract_dictionary


def review_documents_from_list(browser, document_list):
    for document in document_list:
        if open_document(browser, document):
            input(f'Document located at {str(document.value)} located,'
                  'please review & press enter to continue...'
                  f'{remaining_documents(document_list, document)}')
        else:
            record_bad_search(abstract_dictionary, document)
            input(f'No document found at {str(document.value)}, '
                  'please review & press enter to continue...'
                  f'{remaining_documents(document_list, document)}')


# def create_abstraction_dictionary(browser, county, target_directory, document_list, download):
#     search_documents_from_list(browser, county, target_directory, document_list, download)
#     return abstract_dictionary


def create_abstraction(browser, county, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract_dictionary = search_documents_from_list(browser, county, target_directory, document_list, download)
    export_document(target_directory, file_name, abstract_dictionary)
    return abstract_dictionary


def execute_program(county, target_directory, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    while continue_prompt(target_directory, file_name, sheet_name):
        target_directory, file_name, sheet_name = \
            request_more_information(target_directory, file_name, sheet_name)
        create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
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
