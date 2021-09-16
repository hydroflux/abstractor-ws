#!/usr/bin/python3
from eagle.transform_document_list import transform_document_list
from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import next_result, record_document
from eagle.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, document_list, document, review):
    record_document(browser, dataframe, document)
    document_found(document_list, document, review)


def download_single_document(browser, target_directory, document_list, document):
    if not download_document(
        browser,
        dataframe,
        target_directory,
        document
    ):  # add document reception number to document instance
        unable_to_download(dataframe, document)
        no_document_downloaded(document_list, document)
    else:
        document_downloaded(document_list, document)
        # document_found document_list, document)
        # => this is probably a leftover from 'download document list'


def handle_single_document(browser, target_directory, document_list, document, review):
    record_single_document(
        browser,
        document_list,
        document,
        review
    )
    if download and not review:
        download_single_document(
            browser,
            target_directory,
            document_list,
            document
        )


def handle_multiple_documents(browser, target_directory, document_list, document, review):
    handle_single_document(
        browser,
        target_directory,
        document_list,
        document,
        review
    )
    for _ in range(1, document.number_results):
        next_result(browser, document)
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review
        )


def handle_search_results(browser, target_directory,
                          document_list, document, review):
    if document.number_results == 1:
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review
        )
    elif document.number_results > 1:
        handle_multiple_documents(
            browser,
            target_directory,
            document_list,
            document,
            review
        )


def search_documents_from_list(browser, target_directory, document_list, review):
    for document in document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(
                browser,
                target_directory,
                document_list,
                document,
                review
            )
        else:
            record_bad_search(dataframe, document)
            no_document_found(document_list, document, review)
        check_length(dataframe)
    return dataframe  # Is this necessary ? ? ?


def execute_program(county, target_directory, document_list, file_name, review=False):
    browser = create_webdriver(target_directory, False)
    transform_document_list(document_list, county)
    account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(
            browser,
            target_directory,
            document_list,
            review
        )
    )
    # logout ???
    bundle_project(target_directory, abstraction)
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
