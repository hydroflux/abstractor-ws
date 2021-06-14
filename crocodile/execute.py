from crocodile.name_search import search_provided_name
from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project, check_length
from settings.general_functions import start_timer
from settings.settings import download, headless
from settings.user_prompts import document_found, no_document_found

from crocodile.login import account_login
from crocodile.logout import logout
from crocodile.open_document import open_document
from crocodile.record import record_document
from crocodile.search import search
from crocodile.download import download_document


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    record_document(browser, dictionary, document)
    if download:
        if not download_document(browser, county, target_directory, document):
            unable_to_download(dictionary, document)
    document_found(start_time, document_list, document)


def record_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    record_single_document(browser, county, target_directory, document_list, document, start_time)
    # Create an application path for recording multiple documents
    # still need to handle the fact that related documents are returned on search
    # probably should just look for exact matches until finding a use case for multiple documents


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
            # Good practice for future use but still need to handle multiple documents returned in a search
        else:
            record_bad_search(dictionary, document)
            no_document_found(start_time, document_list, document)
        check_length(dictionary)
    return dictionary


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dictionary = search_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dictionary)
    bundle_project(target_directory, abstraction)
    browser.close()


def perform_name_search(browser, county, target_directory, search_name):
    search_provided_name(browser, search_name)
    document_list = create_document_list(browser, search_name)
    search_documents_from_list(browser, county, target_directory, document_list)


def execute_name_search(county, target_directory, search_name):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dictionary = perform_name_search(browser, county, target_directory, search_name)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dictionary)
    bundle_project(target_directory, abstraction)
    browser.close()


def execute_review():
    pass
