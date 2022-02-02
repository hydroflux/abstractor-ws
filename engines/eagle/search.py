# from eagle.error_handling import check_for_error
from project_management.timers import naptime

from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url

from engines.eagle.error_handling import check_for_error
from engines.eagle.login import check_login_status

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


def clear_search(browser, document):
    for id in document.input_attributes:
        clear_input(browser, locate_input, document.input_attributes[id], f'{id} Input', document)


# Same as rattlesnake
def handle_document_value_numbers(browser, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_input, document.input_attributes["Reception Number"],
                          "reception number input", value, document)
        # If having issues, replace with the 'handle_xxx_search_field' functions
    elif document.type == "book_and_page":
        enter_input_value(browser, locate_input, document.input_attributes["Book"],
                          "book input", value[0], document)
        enter_input_value(browser, locate_input, document.input_attributes["Page"],
                          "page input", value[1], document)


def execute_search(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_input, document.button_attributes["Submit Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "document search page")
    check_login_status(browser)
    if not check_for_error(browser, document, 'search'):
        clear_search(browser, document)
        naptime()  # Consider testing without this nap to see if necessary
        execute_search(browser, document)
