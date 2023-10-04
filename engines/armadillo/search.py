from project_management.timers import naptime

from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url

from engines.armadillo.error_handling import check_for_error
# from engines.armadillo.login import check_login_status


def clear_search(browser, abstract, document):
    for id in abstract.county.inputs:
        clear_input(browser, locate_input, abstract.county.inputs[id],
                    f'{id} Input', document)


def handle_document_value_numbers(browser, abstract, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_input, abstract.county.inputs["Reception Number"],
                          "reception number input", value, document)
    elif document.type == "book_and_page":
        enter_input_value(browser, locate_input, abstract.county.inputs["Book"],
                          "book input", value[0], document)
        enter_input_value(browser, locate_input, abstract.county.inputs["Volume"],
                          "volume input", value[0], document)
        enter_input_value(browser, locate_input, abstract.county.inputs["Page"],
                          "page input", value[1], document)


def execute_search(browser, abstract, document):
    handle_document_value_numbers(browser, abstract, document)
    click_button(browser, locate_input, abstract.county.buttons["Submit Search"],
                 "execute search button", document)


def open_search(browser, abstract, document):
    print(f'Searching for document located at {document.extrapolate_value()}')
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "document search page")
    # check_login_status(browser, abstract)


def search(browser, abstract, document):
    open_search(browser, abstract, document)
    if not check_for_error(browser, abstract, document, 'search'):
        clear_search(browser, abstract, document)
        naptime()  # Consider testing without this nap to see if necessary
        execute_search(browser, abstract, document)
        # naptime()
