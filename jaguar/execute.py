from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      create_document_directory,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer

from jaguar.download import download_document
from jaguar.login import account_login
from jaguar.open_document import open_document
from jaguar.record import record
from jaguar.search import search
from jaguar.transform import transform_document_list


def download_recorded_document(browser, document_directory, document_list, document):
    if not download_document(
        browser,
        document_directory,
        document
    ):
        unable_to_download(abstract.dataframe, document)
        no_document_downloaded(document_list, document)
    else:
        document_downloaded(document_list, document)


def handle_single_document(browser, abstract, document):
    record(browser, abstract.dataframe, document)
    document_found(abstract.document_list, document, abstract.review)
    if abstract.download and not abstract.review:
        document_directory = create_document_directory(abstract.target_directory)
        download_recorded_document(
            browser,
            document_directory,
            abstract.document_list,
            document
        )


def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(
            browser,
            abstract,
            document
        )
    elif document.number_results > 1:
        print('Application not equipped to handle multiple documents at the moment; '
              'Script should not have reached this point, please review...')
        input()


def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(
                browser,
                abstract,
                document
            )
        else:
            record_bad_search(abstract, document)


def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    print("file_name", abstract.file_name)
    search_documents_from_list(browser, abstract)
    abstract.abstraction = export_document(
            abstract.county,
            abstract.target_directory,
            abstract.file_name,
            abstract.dataframe
    )
    bundle_project(abstract)
    browser.close()
