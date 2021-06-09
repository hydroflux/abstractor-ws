from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import no_document_image, record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project
from settings.general_functions import start_timer
from settings.settings import download, headless
from settings.user_prompts import document_found, no_document_found

from crocodile.login import account_login
from crocodile.logout import logout
from crocodile.open_document import open_document
from crocodile.record import record_document
from crocodile.search import search


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    document_number, document_image_available = record_document(browser, dictionary, document)
    if download:
        # if not download_document(browser, county, target_directory, document, document_number):
            no_document_image(dictionary, document)
    document_found(start_time, document_list, document)


def record_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    pass


def handle_search_results(browser, county, target_directory, document_list, document, start_time):
    if document.number_results == 1:
        record_single_document()
    elif document.number_results > 1:
        record_multiple_documents()


def search_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, document_list, document, start_time)


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dictionary = search_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dictionary)
    bundle_project(target_directory, abstraction)
    browser.close()


def execute_review(county, target_directory, document_list, file_name):
    pass
