from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import no_document_image, record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document, export_hyperlinks
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download, headless

from armadillo.download import download_document
from armadillo.login import account_login
from armadillo.logout import logout
from armadillo.open_document import open_document
from armadillo.record import build_document_download_information, record
from armadillo.search import search
from armadillo.transform import transform_document_list


def record_document(browser, document_list, document, review):
    record(browser, dataframe, document)
    document_found(document_list, document, review)


def download_recorded_document(browser, target_directory, dataframe, document_list,
                               document, download_only, result_number):
    if not download_document(
        browser,
        target_directory,
        dataframe,
        document,
        result_number
    ):
        no_document_image(dataframe, document)
        no_document_downloaded(document_list, document, download_only)
    else:
        document_downloaded(document_list, document, download_only)


def handle_single_document(browser, target_directory, document_list, document, review, download_only, result_number=0):
    if not download_only:
        record_document(
            browser,
            document_list,
            document,
            review
        )
    else:
        build_document_download_information(
            browser,
            dataframe,
            document)
    if download and not review or download_only:
        download_recorded_document(
            browser,
            target_directory,
            dataframe,
            document_list,
            document,
            download_only,
            result_number
        )


def handle_multiple_documents(browser, target_directory, document_list, document, review, download_only):
    for result_number in range(1, document.number_results):
        search(browser, document)
        if open_document(browser, document, result_number):
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
    handle_single_document(
        browser,
        target_directory,
        document_list,
        document,
        review,
        download_only
    )
    if document.number_results > 1:
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
    return dataframe


def process_dataframe(county, target_directory, file_name, review, download_only):
    if not review:
        if not download_only:
            check_length(dataframe)
            abstraction_file = export_document(county, target_directory, file_name, dataframe)
        else:
            abstraction_file = export_hyperlinks(county, target_directory, file_name, dataframe)
        bundle_project(target_directory, abstraction_file)


def execute_program(county, target_directory, document_list, file_name, review=False, download_only=False):
    browser = create_webdriver(target_directory, headless)
    transform_document_list(document_list, county)
    account_login(browser)
    search_documents_from_list(
            browser,
            target_directory,
            document_list,
            review,
            download_only
        )
    process_dataframe(county, target_directory, file_name, review, download_only)
    logout(browser)
    browser.close()
