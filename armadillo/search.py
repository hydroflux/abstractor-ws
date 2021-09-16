

from selenium_utilities.search import clear_input, enter_input_value
from selenium_utilities.search import locate_input_by_id as locate_input

from settings.file_management import document_value
from settings.general_functions import javascript_script_execution

from armadillo.armadillo_variables import (document_search_url,
                                           execute_document_search_script)
from armadillo.validation import verify_document_search_page_loaded


# Armadillo & rattlesnake identical
def open_document_search(browser):
    browser.get(document_search_url)


def clear_search(browser, document):
    clear_input(browser, document, locate_input, "reception number", document.input_ids["Reception Number"])
    clear_input(browser, document, locate_input, "volume", document.input_ids["Volume"])
    clear_input(browser, document, locate_input, "page", document.input_ids["Page"])


def execute_search(browser):
    javascript_script_execution(browser, execute_document_search_script)


def handle_document_value_numbers(browser, document):
    value = document_value(document)
    if document.type == 'document_number':
        enter_input_value(browser, document, locate_input, document.type, document.input_ids["Reception Number"], value)
    elif document.type == 'volume_and_page':
        enter_input_value(browser, document, locate_input, document.type, document.input_ids["Volume"], value[0])
        enter_input_value(browser, document, locate_input, document.type, document.input_ids["Page"], value[1])
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


def document_search(browser, document):
    handle_document_value_numbers(browser, document)
    execute_search(browser)


def search(browser, document):
    open_document_search(browser)
    verify_document_search_page_loaded(browser, document)
    clear_search(browser, document)
    document_search(browser, document)
