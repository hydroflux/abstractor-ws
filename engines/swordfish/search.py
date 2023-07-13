from selenium.webdriver.support.ui import Select
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element, locate_element_by_class_name,
                                         locate_element_by_id)
from selenium_utilities.open import open_url
from selenium.common.exceptions import NoSuchElementException

# Exact same functionality as "octopus" & "dolphin"


def handle_continuing_collection_search(browser, abstract, document):
    if abstract.document_list.index(document) > 0:
        browser.back()


def select_book_value(browser, abstract, document):
    book = document.document_value()[0].zfill(4)
    try:
        book_selector = Select(
            locate_element(browser, "id", abstract.county.inputs["Book"], "book selector",
                        clickable=True, document=document)
        )
        book_selector.select_by_visible_text(str(book))
        return True
    except NoSuchElementException:
        return False


def select_page_value(browser, abstract, document):
    page = document.document_value()[1]

    enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Page"],
                      "page input", page, document)


def handle_search_values(browser, abstract, document):
    if abstract.program == "legal":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Section"],
                          "section input", abstract.legal[0])
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Township"],
                          "township input", f'T{abstract.legal[1]}N')
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Range"],
                          "range input", f'R{abstract.legal[2]}W')
        return True
    else:
        if document.type == "document_number":
            enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                              "reception number input", document.document_value(), document)
            return True
        elif document.type == "book_and_page":
            if select_book_value(browser, abstract, document):
                select_page_value(browser, abstract, document)
                return True
        else:
            print(f'Abstractor path has not yet been developed to "handle search values" for document type "\
                {document.type}", please review...')
            input()


def execute_search(browser, abstract, document):
    if handle_search_values(browser, abstract, document):
        click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                    "execute search button", document)


def search(browser, abstract, document=None):
    if abstract.number_search_results:
        handle_continuing_collection_search(browser, abstract, document)
    else:
        open_url(browser, abstract.county.urls["Search Page"],
                 abstract.county.titles["Search Page"], "search page")
        execute_search(browser, abstract, document)
