from engines.buffalo.frame_handling import (switch_to_main_frame,
                                            switch_to_search_input_frame,
                                            switch_to_search_menu_frame)
from engines.buffalo.validation import page_is_loaded

from selenium_utilities.element_interaction import get_element_class
from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)


def open_search_page(browser, abstract, document):
    browser.refresh()
    switch_to_main_frame(browser, abstract)
    search_page_button = locate_element_by_id(browser, abstract.county.buttons["Search Menu"],
                                              "search button", True, document)
    search_page_button.click()


def verify_search_page_loaded(browser, abstract):
    header_text = abstract.county.messages["Search Input"]
    return page_is_loaded(browser, abstract, header_text)


def menu_is_active(abstract, menu):
    if get_element_class(menu).endswith(abstract.county.classes["Search Menu Active"]):
        return True


def handle_document_search_menu(browser, abstract, document):
    document_search_menu = locate_element_by_id(browser, abstract.county.buttons["Document Search Menu"],
                                                "document search menu", True, document)
    while not menu_is_active(abstract, document_search_menu):
        document_search_menu.click()


def open_document_search_menu(browser, abstract, document):
    switch_to_search_menu_frame(browser, abstract)
    handle_document_search_menu(browser, abstract, document)


# def clear_double_entry(browser, document):
#     value = document_value(document)
#     if get_field_value(get_document_search_field(browser, document)) == f'{value}{value}':
#         clear_document_search_field(browser, document)


def clear_document_search_field(browser, abstract, document):
    switch_to_search_input_frame(browser, abstract)
    clear_input(browser, locate_element_by_class_name, abstract.county.inputs["Reception Number"],
                "document search field", document)


# def enter_document_number(browser, document):
#     while get_field_value(get_document_search_field(browser, document)) != document_value(document):
#         clear_double_entry(browser, document)
#         get_document_search_field(browser, document).send_keys(Keys.UP + document_value(document))


def handle_document_value_numbers(browser, abstract, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_class_name, abstract.county.inputs["Reception Number"],
                          "reception number input", value, document)
    # elif document.type == "book_and_page":
    #     enter_input_value(browser, locate_element_by_class_name, abstract.county.inputs["Book"],
    #                       "book input", value[0], document)
    #     enter_input_value(browser, locate_element_by_class_name, abstract.county.inputs["Page"],
    #                       "page input", value[1], document)


def execute_search(browser, abstract, document):
    switch_to_search_menu_frame(browser, abstract)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Submit Search"],
                 "search button", document)


def document_search(browser, abstract, document):
    open_document_search_menu(browser, abstract, document)
    clear_document_search_field(browser, abstract, document)
    handle_document_value_numbers(browser, abstract, document)
    execute_search(browser, abstract, document)


def process_document_search(browser, abstract, document):
    if document.type == "document_number":
        document_search(browser, abstract, document)
    else:
        print(f'Unable to search "{document.type}", new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def search(browser, abstract, document):
    open_search_page(browser, abstract, document)
    if verify_search_page_loaded(browser, abstract):
        process_document_search(browser, abstract, document)
