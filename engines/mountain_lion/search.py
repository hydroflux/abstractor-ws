from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)

from settings.general_functions import javascript_script_execution

from engines.mountain_lion.iframe_handling import (
    switch_to_main_frame, switch_to_search_input_frame,
    switch_to_search_menu_frame)
from engines.mountain_lion.validation import page_is_loaded


def open_search_page(browser, abstract, document):
    browser.refresh()
    switch_to_main_frame(browser, abstract)
    click_button(browser, locate_element_by_id,
                 abstract.county.buttons['Open Search'], "open search", document)


def menu_is_active(abstract, menu):
    if menu.get_attribute("class").endswith(abstract.county.classes["Active"]):
        return True


# Use leopard as a guide when adding book & page routes
def open_search_type_tab(browser, abstract, document):
    switch_to_search_menu_frame(browser, abstract)
    document_search_menu = locate_element_by_id(browser, abstract.county.buttons['Document Search Menu'],
                                                'document search menu button', True, document)
    while not menu_is_active(document_search_menu):
        document_search_menu.click()


# Use leopard as a guide when adding book & page routes
def clear_search(browser, abstract, document):
    switch_to_search_input_frame(browser, abstract)
    if document.type == "document_number":
        clear_input(browser, locate_element_by_class_name, abstract.county.inputs["Reception Number"],
                    "document search field", document)
    # else:


# If running into issues, look at the buffalo search script for this function
# def clear_double_entry(browser, abstract, document):
#     pass


# Use leopard as a guide when adding book & page routes
def enter_input(browser, abstract, document):
    if document.type == 'document_number':
        enter_input_value(browser, locate_element_by_class_name, abstract.county.inputs["Reception Number"],
                          "document search field", document)
    # else:


# Use leopard as a guide when adding book & page routes
def execute_search(browser, abstract):
    switch_to_search_menu_frame(browser, abstract)
    javascript_script_execution(browser, abstract.county.scripts["Search"])


# Use leopard as a guide when adding book & page routes
def execute_document_number_search(browser, abstract, document):
    open_search_type_tab(browser, abstract, document)
    # clear_search(browser, abstract, document)
    enter_input(browser, abstract, document)
    execute_search(browser, abstract)


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
