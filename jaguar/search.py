from selenium_utilities.inputs import clear_input, click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_id
from selenium_utilities.open import open_url

from settings.county_variables.jaguar import search_url, search_title


def clear_search(browser, document):
    for attribute in document.input_attributes:
        clear_input(browser, locate_element_by_id, document.input_attributes[attribute],
                    f'{attribute} Input', document)


def handle_document_value_numbers(browser, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_id, document.input_attributes["Reception Number"],
                          "reception number input", value, document)
    else:
        print(f'Unable to search "{document.extrapolate_value()}" document type "{document.type}".')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_element_by_class_name, document.button_attributes["Submit Search"],
                 "execute search button", document)


def search(browser, document):
    open_url(browser, search_url, search_title, "document search page")
    clear_search(browser, document)
    execute_search(browser, document)
