from engines.mountain_lion.iframe_handling import switch_to_main_frame
from engines.mountain_lion.validation import page_is_loaded
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id


def open_search_page(browser, abstract, document):
    browser.refresh()
    switch_to_main_frame(browser, abstract)
    click_button(browser, locate_element_by_id,
                 abstract.county.buttons['Open Search'], "open search", document)


# Use leopard as a guide when adding book & page routes
def open_search_type_tab(browser, abstract, document):
    pass


# Use leopard as a guide when adding book & page routes
def clear_search(browser, abstract, document):
    pass


# Use leopard as a guide when adding book & page routes
def enter_input(browser, abstract, document):
    pass


# Use leopard as a guide when adding book & page routes
def execute_search(browser, abstract, document):
    pass


# Use leopard as a guide when adding book & page routes
def execute_document_number_search(browser, abstract, document):
    pass


def handle_document_search(browser, abstract, document):
    if document.type == "document_number":
        execute_document_number_search(browser, abstract, document)
    else:
        print(f'Unable to search "{document.type}" document type, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def search(browser, abstract, document):
    open_search_page(browser, abstract, document)
    if page_is_loaded(browser, abstract, abstract.county.messages['Search Header']):
        handle_document_search(browser, abstract, document)
