from engines.rattlesnake.download_early_documents import download_early_documents
from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.invalid import no_document_image, record_invalid_search
from settings.driver import create_webdriver
from project_management.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download, headless

from engines.rattlesnake.download import download_document
from engines.rattlesnake.login import account_login
from engines.rattlesnake.logout import logout
from engines.rattlesnake.open_document import open_document
from engines.rattlesnake.record import record
from engines.rattlesnake.search import search
from engines.rattlesnake.transform import transform_document_list


def record_document(browser, document_list, document, review):
    record(browser, dataframe, document)
    document_found(document_list, document, review)


def download_recorded_document(browser, target_directory, document_list, document):
    if not download_document(
        browser,
        target_directory,
        document
    ):
        no_document_image(abstract, document)
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
        download_recorded_document(
            browser,
            target_directory,
            document_list,
            document
        )


def handle_multiple_documents(browser, target_directory, document_list, document, review):
    for result_number in range(1, document.number_results):
        search(browser, document)
        open_document(browser, document, result_number)
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review
        )


def handle_search_results(browser, target_directory, document_list, document, review):
    if open_document(browser, document):
        handle_single_document(
            browser,
            target_directory,
            document_list,
            document,
            review
        )
        if document.number_results > 1:
            handle_multiple_documents(
                browser,
                target_directory,
                document_list,
                document,
                review
            )
    else:
        record_invalid_search(dataframe, document)
        no_document_found(document_list, document, review)


def search_documents_from_list(browser, target_directory, document_list, review):
    for document in document_list:
        document.start_time = start_timer()
        search(browser, document)
        handle_search_results(
            browser,
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
    search_documents_from_list(browser, target_directory, document_list, review)
    if not review:
        abstraction = export_document(
            county,
            target_directory,
            file_name,
            dataframe
        )
        bundle_project(target_directory, abstraction)
    logout(browser)
    browser.close()


def execute_early_document_download(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    transform_document_list(document_list, county, True)
    account_login(browser)
    download_early_documents(browser, target_directory, document_list)
    browser.close()