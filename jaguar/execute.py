from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      create_document_directory,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from jaguar.download import download_document
from jaguar.login import account_login
from jaguar.open_document import open_document
from jaguar.record import record
from jaguar.search import search
from jaguar.transform import transform_document_list


def record_document(browser, document_list, document, review):
    record(browser, dataframe, document)
    document_found(document_list, document, review)


def download_recorded_document(browser, document_directory, document_list, document):
    if not download_document(
        browser,
        document_directory,
        document
    ):
        unable_to_download(dataframe, document)
        no_document_downloaded(document_list, document)
    else:
        document_downloaded(document_list, document)


def handle_single_document(browser, target_directory, document_list, document, review):
    record_document(
        browser,
        document_list,
        document,
        review
    )
    if download and not review:
        document_directory = create_document_directory(target_directory)
        download_recorded_document(
            browser,
            document_directory,
            document_list,
            document
        )


def handle_search_results(browser, target_directory, document_list, document, review):
    if document.number_results == 1:
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review
        )
    elif document.number_results > 1:
        print('Application not equipped to handle multiple documents at the moment; '
              'Script should not have reached this point, please review...')
        input()


def handle_bad_search(dataframe, document_list, document, review):
    record_bad_search(dataframe, document)
    no_document_found(document_list, document, review)


def search_documents_from_list(browser, target_directory, document_list, dataframe, review):
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
            handle_bad_search(dataframe, document_list, document, review)


def execute_program(headless, county, target_directory, document_list, file_name, review=False):
    browser = create_webdriver(target_directory, headless)
    transform_document_list(document_list, county)
    account_login(browser)
    search_documents_from_list(
            browser,
            target_directory,
            document_list,
            dataframe,
            review
        )
    abstraction = export_document(
            county,
            target_directory,
            file_name,
            dataframe
    )
    bundle_project(target_directory, abstraction)
    browser.close()
