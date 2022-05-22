from selenium_utilities.inputs import clear_input, click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_id
from selenium_utilities.open import open_url


def clear_search(browser, abstract, document):
    for attribute in abstract.county.inputs:
        clear_input(browser, locate_element_by_id, abstract.county.inputs[attribute],
                    f'{attribute} Input', document)


def handle_document_value_numbers(browser, abstract, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                          "reception number input", value, document)
    else:
        print(f'Unable to search "{document.extrapolate_value()}" document type "{document.type}".')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, abstract, document):
    handle_document_value_numbers(browser, abstract, document)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_url(browser, abstract.county.urls["Search"],
             abstract.county.titles["Search"], "document search page")
    clear_search(browser, abstract, document)
    execute_search(browser, abstract, document)
