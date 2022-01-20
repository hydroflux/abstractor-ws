#!/usr/bin/python3
from settings.bad_search import record_bad_search
from settings.download_management import previously_downloaded
from settings.driver import create_webdriver
from settings.export import export_document
from settings.general_functions import start_timer

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import next_result, record
from eagle.search import search
from eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def handle_single_document(browser, abstract, document):
    record(browser, abstract, document)
    if abstract.download and not abstract.review:
        if document.number_results == 1:
            if previously_downloaded(abstract.document_directory, document):
                return
        download_document(browser, abstract, document)


def handle_multiple_documents(browser, abstract, document):
    handle_single_document(browser, abstract, document)
    for result_number in range(1, document.number_results):
        document.result_number = result_number
        next_result(browser, document)
        handle_single_document(browser, abstract, document)


# Identical to 'jaguar' execute_program
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document)


# Identical to 'jaguar' execute_program
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_bad_search(abstract, document)


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
