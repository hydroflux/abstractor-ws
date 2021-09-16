from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download, headless

from rattlesnake.download import download_document
from rattlesnake.login import account_login
from rattlesnake.logout import logout
from rattlesnake.open_document import open_document
from rattlesnake.record import record
from rattlesnake.search import search
from rattlesnake.transform_document_list import transform_document_list


def record_document(browser, document_list, document, review, result_number):
    record(browser, dataframe, document, result_number)
    document_found(document_list, document, review)


def download_recorded_document(browser, county, target_directory, document_list, document):
    if not download_document(
        browser,
        county,
        target_directory,
        document
    ):
        unable_to_download(dataframe, document)
        no_document_downloaded(document_list, document)
    else:
        document_downloaded(document_list, document)


def handle_single_document(browser, county, target_directory, document_list, document, review, result_number=None):
    record_document(
        browser,
        document_list,
        document,
        review,
        result_number
    )
    if download and not review:
        download_recorded_document(
            browser,
            county,
            target_directory,
            document_list,
            document
        )


def handle_multiple_documents(browser, county, target_directory, document_list, document, review):
    for result_number in range(1, document.number_results):
        search(browser, document)
        open_document(browser, document, result_number)
        handle_single_document(
            browser,
            county,
            target_directory,
            document_list,
            document,
            review,
            result_number
        )


def handle_search_results(browser, county, target_directory, document_list, document, review):
    if open_document(browser, document):
        handle_single_document(
            browser,
            county,
            target_directory,
            document_list,
            document,
            review
        )
        if document.number_results > 1:
            handle_multiple_documents(
                browser,
                county,
                target_directory,
                document_list,
                document,
                review
            )
    else:
        record_bad_search(dataframe, document)
        no_document_found(document_list, document, review)


def search_documents_from_list(browser, county, target_directory, document_list, review):
    for document in document_list:
        document.start_time = start_timer()
        search(browser, document)
        handle_search_results(
            browser,
            county,
            target_directory,
            document_list,
            document,
            review
        )
        check_length(dataframe)
    return dataframe


def execute_program(county, target_directory, document_list, file_name, review=False):
    browser = create_webdriver(target_directory, headless)
    transform_document_list(document_list, county)
    account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(
            browser,
            county,
            target_directory,
            document_list,
            review
        )
    )
    logout(browser)
    bundle_project(target_directory, abstraction)
    browser.close()
