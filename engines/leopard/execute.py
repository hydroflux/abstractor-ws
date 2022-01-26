#!/usr/bin/python3
from project_management.export import export_document

from settings.driver import create_webdriver
from settings.general_functions import start_timer
from settings.invalid import record_invalid_search

from engines.leopard.download import download_document
from engines.leopard.login import account_login
from engines.leopard.logout import logout
from engines.leopard.open_document import open_document
from engines.leopard.record import next_result, record
from engines.leopard.search import search
from engines.leopard.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Nearly to 'eagle' handle_single_document
def handle_single_document(browser, abstract, document):
    record(browser, abstract, document)
    if abstract.download:
        download_document(browser, abstract, document)


# Identical to 'eagle' handle_multiple_documents
def handle_multiple_documents(browser, abstract, document):
    handle_single_document(browser, abstract, document)
    for result_number in range(1, document.number_results):
        document.result_number = result_number  # Pulled from 'eagle' execute, currently unused
        next_result(browser, document)
        handle_single_document(browser, abstract, document)


# Identical to 'eagle' and 'jaguar' handle_search_results
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document)


# Identical to 'eagle', 'tiger', & 'jaguar' search_documents_from_list
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        # naptime()  # --- script runs without issues while this nap was in place
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_invalid_search(abstract, document)
        # check_length(dataframe)  # Where is the best place to put this???


def execute_program(abstract):
    if abstract.download_only:
        abstract.headless = False  # Figure out better placement
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    logout(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()
