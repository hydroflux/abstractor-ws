from engines.buffalo.frame_handling import (switch_to_main_frame,
                                            switch_to_search_input_frame,
                                            switch_to_search_menu_frame)
from engines.buffalo.validation import page_is_loaded

from selenium_utilities.element_interaction import get_element_class
from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import (locate_element_by_xpath,
                                         locate_element_by_id, locate_element)


def open_search_page(browser, abstract, document):
    browser.refresh()
    switch_to_main_frame(browser, abstract)
    search_page_button = locate_element(browser, "id", abstract.county.buttons["Search Menu"],
                                        "search button", True, document)
    search_page_button.click()


def verify_search_page_loaded(browser, abstract):
    header_text = abstract.county.messages["Search Input"]
    return page_is_loaded(browser, abstract, header_text)


def menu_is_active(abstract, menu):
    if get_element_class(menu).endswith(abstract.county.classes["Search Menu Active"]):
        return True


def open_search_menu(browser, abstract, document, menu_id):
    switch_to_search_menu_frame(browser, abstract)
    search_menu = locate_element(browser, "id", menu_id, "document search menu", True, document)
    while not menu_is_active(abstract, search_menu):
        search_menu.click()


def clear_document_search_field(browser, abstract, document, inputs):
    switch_to_search_input_frame(browser, abstract)
    for input in inputs:
        clear_input(browser, locate_element_by_xpath, input, "search field input", document)


def handle_document_value_numbers(browser, abstract, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_xpath, abstract.county.inputs["Reception Number"],
                          "reception number input", value, document)
    elif document.type == "book_and_page":
        enter_input_value(browser, locate_element_by_xpath, abstract.county.inputs["Book"],
                          "book input", value[0], document)
        enter_input_value(browser, locate_element_by_xpath, abstract.county.inputs["Page"],
                          "page input", value[1], document)


def process_document_search(browser, abstract, document):
    if document.type == "document_number":
        reception_number_input_attribute = abstract.county.inputs["Reception Number"]
        open_search_menu(browser, abstract, document, abstract.county.buttons["Document Search Menu"])
        clear_document_search_field(browser, abstract, document, [reception_number_input_attribute])
    elif document.type == "book_and_page":
        book_input_attribute = abstract.county.inputs["Book"]
        page_input_attribute = abstract.county.inputs["Page"]
        open_search_menu(browser, abstract, document, abstract.county.buttons["Book & Page Search Menu"])
        clear_document_search_field(browser, abstract, document, [book_input_attribute, page_input_attribute])
    else:
        print(f'Unable to search "{document.type}", new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, abstract, document):
    switch_to_search_menu_frame(browser, abstract)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Search"],
                 "search button", document)


def search(browser, abstract, document):
    open_search_page(browser, abstract, document)
    if verify_search_page_loaded(browser, abstract):
        process_document_search(browser, abstract, document)
        handle_document_value_numbers(browser, abstract, document)
        execute_search(browser, abstract, document)
