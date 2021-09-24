from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url

from rattlesnake.rattlesnake_variables import search_title, search_url


def clear_search(browser, document):
    for id in document.input_ids:
        clear_input(browser, locate_input, document.input_ids[id], f'{id} Input', document)


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


def search(browser, document):
    open_url(browser, search_url, search_title, "document search", document)  # Open Document Search
    # verify_document_search_page_loaded(browser, search_url, open_document_search)
    clear_search(browser, document)
    handle_document_value_numbers(browser, document)  # Enter Value Numbers
    click_button(browser, locate_input, document.button_ids["Submit Button"],
                 "submit button", document)  # Execute Search
