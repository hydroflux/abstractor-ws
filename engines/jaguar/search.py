from project_management.timers import naptime

from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url


def clear_search(browser, abstract, document):
    for id in abstract.county.inputs:
        clear_input(browser, locate_input, abstract.county.inputs[id],
                    f'{id} Input', document)


def handle_document_value_numbers(browser, abstract, document):
    if document.type == "document_number":
        enter_input_value(browser, locate_input, abstract.county.inputs["Reception Number"],
                          "reception number input", document.document_value(), document)
    elif document.type == "name":
        enter_input_value(browser, locate_input, abstract.county.inputs["Name"],
                          "name input", document.document_value(), document)
        enter_input_value(browser, locate_input, abstract.county.inputs["Start Date"],
                          "start date input", abstract.start_date, document)
        enter_input_value(browser, locate_input, abstract.county.inputs["End Date"],
                          "end date input", abstract.end_date, document)


def execute_search(browser, abstract, document):
    handle_document_value_numbers(browser, abstract, document)
    click_button(browser, locate_input, abstract.county.buttons["Submit Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "document search page")
    clear_search(browser, abstract, document)
    naptime()  # Consider testing without this nap to see if necessary
    execute_search(browser, abstract, document)
