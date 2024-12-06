from selenium.webdriver.support.ui import Select
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id, select_dropdown_option_by_value)
from selenium_utilities.open import open_url
from selenium.common.exceptions import NoSuchElementException

# Similar code functionality in "dolphin", "manta_ray", "octopus" & "swordfish"


def handle_continuing_collection_search(browser, abstract, document):
    if abstract.document_list.index(document) > 0:
        browser.back()


def handle_search_values(browser, abstract, document):
    if abstract.program == "legal":
        select_dropdown_option_by_value(browser, "id", abstract.county.inputs["Section"], "section input", abstract.legal[0])
        select_dropdown_option_by_value(browser, "id", abstract.county.inputs["Township"], "township input", f'T{abstract.legal[1]}')
        select_dropdown_option_by_value(browser, "id", abstract.county.inputs["Range"], "range input", f'R{abstract.legal[2]}')
    else:
        value = document.document_value()
        if document.type == "document_number":
            enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                              "reception number input", value, document)
        elif document.type == "book_and_page":
            enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Book"],
                              "book input", value[0].zfill(4), document)
            enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Page"],
                              "page input", value[1], document)
        else:
            print(f'Abstractor path has not yet been developed to "handle search values" for document type "\
                {document.type}", please review...')
            input()


def execute_search(browser, abstract, document):
    handle_search_values(browser, abstract, document)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document)


def search(browser, abstract, document=None):
    if abstract.number_search_results:
        handle_continuing_collection_search(browser, abstract, document)
    else:
        open_url(browser, abstract.county.urls["Search Page"],
                    abstract.county.titles["Search Page"], "search page")
        execute_search(browser, abstract, document)
