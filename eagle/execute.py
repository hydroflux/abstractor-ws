#!/usr/bin/python3
from eagle.record import build_document_download_information
from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_last_document,
                                      check_length, document_downloaded,
                                      document_found, no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import next_result, record
from eagle.search import search
from eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_document(browser, document_list, document, review):
    record(browser, dataframe, document)
    document_found(document_list, document, review)


def download_recorded_document(browser, target_directory, document_list, document, download_only, result_number):
    if not download_document(
        browser,
        dataframe,
        target_directory,
        document,
        result_number
    ):  # add document reception number to document instance
        unable_to_download(dataframe, document)
        no_document_downloaded(document_list, document, download_only)
    else:
        document_downloaded(document_list, document, download_only)
        # document_found document_list, document)
        # => this is probably a leftover from 'download document list'


def handle_single_document(browser, target_directory, document_list, document, review, download_only, result_number=0):
    if not download_only:
        record_document(
            browser,
            document_list,
            document,
            review
        )
    else:
        build_document_download_information(browser, dataframe, document)
    if download and not review:
        download_recorded_document(
            browser,
            target_directory,
            document_list,
            document,
            download_only,
            result_number
        )


def handle_multiple_documents(browser, target_directory, document_list, document, review, download_only):
    handle_single_document(
        browser,
        target_directory,
        document_list,
        document,
        review,
        download_only
    )
    for result_number in range(1, document.number_results):
        next_result(browser, document)
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review,
            download_only,
            result_number
        )


def handle_search_results(browser, target_directory, document_list, document, review, download_only):
    if document.number_results == 1:
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review,
            download_only
        )
    elif document.number_results > 1:
        handle_multiple_documents(
            browser,
            target_directory,
            document_list,
            document,
            review,
            download_only
        )


def handle_bad_search(dataframe, document_list, document, review, download_only):
    if not download_only:
        record_bad_search(dataframe, document)
    no_document_found(document_list, document, review)


def search_documents_from_list(browser, target_directory, document_list, review, download_only):
    for document in document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(
                browser,
                target_directory,
                document_list,
                document,
                review,
                download_only
            )
        else:
            handle_bad_search(dataframe, document_list, document, review, download_only)
        check_length(dataframe)
        check_last_document(dataframe, document_list, document)
    return dataframe  # Is this necessary ? ? ?


def execute_program(county, target_directory, document_list, file_name, review=False, download_only=False):
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
            review,
            download_only
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
