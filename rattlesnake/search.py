from selenium_utilities.search import clear_input, click_button, locate_input_by_id as locate_input

from settings.general_functions import get_field_value

from rattlesnake.rattlesnake_variables import (document_search_field_id,
                                               document_search_url,
                                               page_search_field_id,
                                               volume_search_field_id)
from rattlesnake.validation import verify_document_search_page_loaded


# Armadillo & rattlesnake identical
def open_document_search(browser):
    browser.get(document_search_url)


def clear_search(browser, document):
    clear_input(browser, document, locate_input, "reception number", document.input_ids["Reception Number"])
    clear_input(browser, document, locate_input, "volume", document.input_ids["Volume"])
    clear_input(browser, document, locate_input, "page", document.input_ids["Page"])


def handle_document_search_field(browser, document, type="reception number", id=document_search_field_id):
    value = document.document_value()
    enter_value_number(browser, document, type, id, value)


def handle_volume_number_search_field(browser, document, volume, type="volume", id=volume_search_field_id):
    enter_value_number(browser, document, type, id, volume)


def handle_page_number_search_field(browser, document, page, type="page", id=page_search_field_id):
    enter_value_number(browser, document, type, id, page)


def handle_volume_page_search_fields(browser, document):
    volume, page = document.document_value()
    handle_volume_number_search_field(browser, document, volume)
    handle_page_number_search_field(browser, document, page)


def execute_search(browser, document):
    click_button(browser, document, document.search_field_id["Submit Button"], "submit button")


def document_search(browser, document):
    handle_document_search_field(browser, document)
    execute_search(browser, document)


def volume_and_page_search(browser, document):
    handle_volume_page_search_fields(browser, document)
    execute_search(browser, document)


def search(browser, document):
    open_document_search(browser)
    verify_document_search_page_loaded(browser, document, open_document_search)
    clear_search(browser, document)
    if document.type == 'document_number':
        document_search(browser, document)
    elif document.type == 'volume_and_page':
        volume_and_page_search(browser, document)
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()
