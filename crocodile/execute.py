from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      display_document_list, document_found,
                                      document_value, no_document_found)
from settings.general_functions import start_timer
from settings.settings import download, headless

from crocodile.download import download_document
from crocodile.login import account_login
from crocodile.logout import logout
from crocodile.name_search import search_provided_name
from crocodile.open_document import (create_name_document_list, next_result,
                                     open_document)
from crocodile.record import record_document
from crocodile.search import search


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    record_document(browser, county, dataframe, document)
    if download:
        if not download_document(browser, county, target_directory, document):
            unable_to_download(dataframe, document)
    document_found(start_time, document_list, document)


def record_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    record_single_document(browser, county, target_directory, document_list, document, start_time)
    for link_index in range(document.number_results - 1):
        next_result(browser, document, link_index)
        record_single_document(browser, county, target_directory, document_list, document, start_time)


def handle_search_results(browser, county, target_directory, document_list, document, start_time):
    if document.number_results == 1:
        record_single_document(browser, county, target_directory, document_list, document, start_time)
    elif document.number_results > 1:
        record_multiple_documents(browser, county, target_directory, document_list, document, start_time)


def search_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, document_list, document, start_time)
        else:
            record_bad_search(dataframe, document)
            no_document_found(start_time, document_list, document)
        check_length(dataframe)
    return dataframe


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dataframe = search_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dataframe)
    bundle_project(target_directory, abstraction)
    browser.close()


def perform_name_search(browser, county, target_directory, search_name):
    search_provided_name(browser, search_name)
    document_list = create_name_document_list(browser, search_name)
    display_document_list(document_list)
    return search_documents_from_list(browser, county, target_directory, document_list)


def execute_name_search(county, target_directory, search_name):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dataframe = perform_name_search(browser, county, target_directory, search_name)
    logout(browser)
    abstraction = export_document(county, target_directory, document_value(search_name), dataframe)
    bundle_project(target_directory, abstraction)
    # sleep(8)  #  <-- use for demo
    browser.close()


def execute_review():
    pass
