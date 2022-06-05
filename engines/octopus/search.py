from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)
from selenium_utilities.open import open_url


def handle_search_values(browser, abstract, document):
    if document.type == "legal":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Section"],
                          "section input", abstract.legal[0])
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Township"],
                          "township input", abstract.legal[1])
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Range"],
                          "range input", abstract.legal[2])
    else:
        print(f'Abstractor path has not yet been developed to "handle search values" for document type "\
               {document.type}", please review...')
        input()


def execute_search(browser, abstract, document):
    handle_search_values(browser, abstract, document)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "search page")
    execute_search(browser, abstract, document)
