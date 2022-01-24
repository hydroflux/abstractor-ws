#!/usr/bin/python3
from settings.invalid import record_invalid_search
from settings.download_management import previously_downloaded
from settings.driver import create_webdriver
from project_management.export import export_document
from settings.general_functions import start_timer

from engines.eagle.download import download_document
from engines.eagle.login import account_login
from engines.eagle.open_document import open_document
from engines.eagle.record import next_result, record
from engines.eagle.search import search
from engines.eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Try to match to the 'leopard' handle_single_document function
def handle_single_document(browser, abstract, document):
    record(browser, abstract, document)
    if abstract.download:
        if document.number_results == 1:
            if previously_downloaded(abstract.document_directory, document):
                return
        download_document(browser, abstract, document)


# Identical to 'leopard' handle_multiple_documents
def handle_multiple_documents(browser, abstract, document):
    handle_single_document(browser, abstract, document)
    for result_number in range(1, document.number_results):
        document.result_number = result_number
        next_result(browser, document)
        handle_single_document(browser, abstract, document)


# Identical to 'jaguar' & 'leopard' handle_search_results
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document)


# Identical to 'jaguar' & 'leopard' search_documents_from_list
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_invalid_search(abstract, document)


# Identical to 'jaguar' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    project = export_document(abstract)
    project.bundle_project(abstract)
    browser.close()


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
