from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input

from rattlesnake.rattlesnake_variables import document_search_url
from rattlesnake.validation import verify_document_search_page_loaded


# Armadillo & rattlesnake identical
def open_document_search(browser):
    browser.get(document_search_url)


def clear_search(browser, document):
    clear_input(browser, locate_input, document.input_ids["Reception Number"],
                "reception number input", document)
    clear_input(browser, locate_input, document.input_ids["Volume"],
                "volume input", document)
    clear_input(browser, locate_input, document.input_ids["Page"],
                "page input", document)


def handle_document_value_numbers(browser, document):
    value = document.document_value()
    if document.type == 'document_number':
        enter_input_value(browser, locate_input, document.input_ids["Reception Number"],
                          "reception number input", value, document)
    elif document.type == 'volume_and_page':
        enter_input_value(browser, locate_input, document.input_ids["Volume"],
                          "volume input", value[0], document)
        enter_input_value(browser, locate_input, document.input_ids["Page"],
                          "page input", value[1], document)
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, document):
    click_button(browser, locate_input, document.button_ids["Submit Button"], "submit button", document)


def document_search(browser, document):
    handle_document_value_numbers(browser, document)
    execute_search(browser, document)


def search(browser, document):
    open_document_search(browser)
    verify_document_search_page_loaded(browser, document, open_document_search)
    clear_search(browser, document)
    document_search(browser, document)
