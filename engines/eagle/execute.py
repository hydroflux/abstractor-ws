#!/usr/bin/python3
from actions.executors import close_program, handle_multiple_documents, handle_single_document
from settings.invalid import record_invalid_search
from settings.driver import create_webdriver
from settings.general_functions import start_timer

from engines.eagle.download import download_document
from engines.eagle.login import account_login
from engines.eagle.open_document import open_document
from engines.eagle.record import next_result, record
from engines.eagle.search import search
from engines.eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'eagle', 'tiger', & 'leopard' handle_search_results
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document, record, download_document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document, record, download_document, next_result)


# Identical to 'jaguar', 'tiger', & 'leopard' search_documents_from_list
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_invalid_search(abstract, document)


# Identical to 'leopard', 'jaguar', & 'tiger' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    close_program(browser, abstract)


# def execute_web_program(client, legal, upload_file):
#     sheet_name = 'Documents'
#     download = False
#     file_name = upload_file
#     target_directory = web_directory
#     headless = False
#     browser = create_webdriver(target_directory, headless)
#     account_login(browser)
#     dataframe = create_abstraction(browser, target_directory, file_name, sheet_name, download)
#     browser.close()
#     return abstract_dictionary
