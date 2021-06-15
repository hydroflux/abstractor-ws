#!/usr/bin/python3
from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, document_found,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import get_reception_number, next_result, record_document
from eagle.search import document_search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, county, target_directory,
                           abstract_dictionary, document_list, document, start_time):
    document_number = record_document(browser, county, abstract_dictionary, document)
    if download:
        download_document(browser, county, abstract_dictionary, target_directory, document, document_number)
    document_found(start_time, document_list, document)


def record_multiple_documents(browser, county, target_directory,
                              abstract_dictionary, document_list, document, start_time):
    record_single_document(browser, county, target_directory,
                           abstract_dictionary, document_list, document, start_time)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        record_single_document(browser, county, target_directory,
                               abstract_dictionary, document_list, document, start_time)


def review_multiple_documents(browser, start_time, document_list, document):
    document_found(start_time, document_list, document, "review")
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        document_found(start_time, document_list, document, "review")


def download_single_document(browser, county, target_directory, document_list, document, start_time):
    document_number = get_reception_number(browser, document)
    download_document(browser, county, abstract_dictionary, target_directory, document, document_number)
    document_found(start_time, document_list, document)


def download_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    download_single_document(browser, county, target_directory, document_list, document, start_time)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        download_single_document(browser, county, target_directory, document_list, document, start_time)


def handle_search_results(browser, county, target_directory,
                          document_list, document, start_time, alt=None):
    if alt is None:
        if document.number_results > 1:
            record_multiple_documents(browser, county, target_directory,
                                      abstract_dictionary, document_list, document, start_time)
        else:
            record_single_document(browser, county, target_directory,
                                   abstract_dictionary, document_list, document, start_time)
    elif alt == 'review':
        if document.number_results > 1:
            review_multiple_documents(browser, start_time, document_list, document)
        else:
            document_found(start_time, document_list, document, "review")
    elif alt == "download":
        if document.number_results > 1:
            download_multiple_documents(browser, county, target_directory, document_list, document, start_time)
        else:
            download_single_document(browser, county, target_directory, document_list, document, start_time)


def search_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        document_search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory,
                                  document_list, document, start_time)
        else:
            record_bad_search(abstract_dictionary, document)
            no_document_found(start_time, document_list, document)
    return abstract_dictionary  # Is this necessary ? ? ?


def create_abstraction(browser, county, target_directory, document_list, file_name):
    abstract_dictionary = search_documents_from_list(browser, county, target_directory, document_list)
    # Is the abstract_dictionary return necessary ? ? ?
    return export_document(county, target_directory, file_name, abstract_dictionary)


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    abstraction = create_abstraction(browser, county, target_directory, document_list, file_name)
    browser.close()
    bundle_project(target_directory, abstraction)


def review_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        document_search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory,
                                  document_list, document, start_time, 'review')
        else:
            no_document_found(start_time, document_list, document, "review")


def download_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        document_search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory,
                                  document_list, document, start_time, 'download')
        else:
            no_document_found(start_time, document_list, document)


def execute_review(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    review_documents_from_list(browser, county, target_directory, document_list)
    browser.close()


def execute_document_download(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    download_documents_from_list(browser, county, target_directory, document_list)
    browser.close()


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
