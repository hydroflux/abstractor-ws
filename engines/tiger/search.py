from engines.tiger.error_handling import check_for_browser_error
from project_management.timers import naptime
from selenium_utilities.element_interaction import (get_parent_element,
                                                    is_active_class)
from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id

from settings.general_functions import javascript_script_execution


def access_search_navigation_tab(browser, abstract, document):
    search_navigation_tab = locate_element_by_id(browser, abstract.county.ids["Search Navigation"],
                                                 "search navigation", True, document)
    while search_navigation_tab is None:
        search_navigation_tab = locate_element_by_id(browser, abstract.county.ids["Search Navigation"],
                                                     "search navigation", True, document)
    return search_navigation_tab


def open_search(browser, abstract, document):
    javascript_script_execution(browser, abstract.county.scripts["Search"])
    navigation_tab = access_search_navigation_tab(browser, abstract, document)
    while not is_active_class(navigation_tab):
        print("Navigation tab not active, attempting to connect again.")
        naptime()  # Allows time for navigation to load
        navigation_tab = access_search_navigation_tab(browser, abstract, document)
    assert abstract.county.titles["Search"]

# def open_search(browser, abstract):
#     # Messy => figure out a better way to do this
#     javascript_script_execution(browser, abstract.county.scripts["Search"])
#     naptime()
#     # This will probably not work great when called during the 'login' process
#     ######
#     search_navigation = locate_element_by_id(browser, abstract.county.ids["Search Navigation"],
#                                              "search navigation", True)
#     if is_active_class(search_navigation):
#         return
#     else:
#         browser.execute_script(abstract.county.scripts["Search"])
#         assert abstract.county.titles["Search"]


def access_search_type_tab_child(browser, document, attribute, type):
    search_type_tab_child = locate_element_by_id(browser, attribute, type, True, document)
    while search_type_tab_child is None:
        check_for_browser_error(browser)
        search_type_tab_child = locate_element_by_id(browser, attribute, type, True, document)
    return search_type_tab_child


def access_search_type_tab(browser, document, attribute, type):
    search_type_tab_child = access_search_type_tab_child(browser, document, attribute, type)
    return get_parent_element(search_type_tab_child)


def open_tab(browser, document, attribute, type):
    tab = access_search_type_tab(browser, document, attribute, type)
    while not is_active_class(tab):
        tab = access_search_type_tab(browser, document, attribute, type)
        tab.click()


def open_search_type_tab(browser, abstract, document):
    if document.type == "document_number":
        open_tab(browser, document, abstract.county.ids["Document Search Tab"], "document search tab")
    elif document.type == "book_and_page":
        open_tab(browser, document, abstract.county.ids["Book And Page Search Tab"], "book and page search tab")
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


# def open_search_tab(browser, abstract):
#     search_tab = locate_element_by_id(browser, abstract.county.ids["Search Tab"],
#                                       "search tab", True)
#     center_element(browser, search_tab)
#     if is_active_class(get_parent_element(search_tab)):
#         return
#     else:
#         search_tab.click()


def clear_search(browser, abstract, document):
    if document.type == "document_number":
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                    "document search field", document)
    elif document.type == "book_and_page":
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Book"],
                    "book search field", document)
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Page"],
                    "page search field", document)


def enter_input(browser, abstract, document):
    if document.type == "document_number":
        # dropped a 'scroll_into_view' before entering inputs => update the 'enter_input_value' function accordingly
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                          "document search field", document.document_value())
    elif document.type == "book_and_page":
        book, page = document.document_value()
        # dropped a 'scroll_into_view' before entering inputs => update the 'enter_input_value' function accordingly
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Book"],
                          "book search field", book, document)
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Page"],
                          "page search field", page, document)


def execute_search(browser, abstract, document):
    if document.type == "document_number":
        click_button(browser, locate_element_by_id, abstract.county.buttons["Document Search"],
                     "document search button", document)
    elif document.type == "book_and_page":
        click_button(browser, locate_element_by_id, abstract.county.buttons["Book And Page Search"],
                     "book and page search button", document)  # Execute Search
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


# def handle_document_value_numbers(browser, abstract, document):
#     value = document.value
#     if document.type == "document_number":
#         enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
#                           "reception number input", value, document)
#     elif document.type == "book_and_page":
#         open_tab(browser, document, abstract.county.ids["Book And Page Search Tab"], "book and page search tab")


# def execute_search(browser, abstract, document):
#     handle_document_value_numbers(browser, abstract, document)
#     click_button(browser, locate_element_by_id, abstract.county.buttons["Search"],
#                  "execute search button", document)


def search(browser, abstract, document):
    open_search(browser, abstract, document)
    open_search_type_tab(browser, abstract, document)
    clear_search(browser, abstract, document)
    enter_input(browser, abstract, document)
    execute_search(browser, abstract, document)


# def search(browser, abstract, document):
#     open_search(browser, abstract)
#     open_search_tab(browser, abstract)
#     clear_search(browser, abstract, document)
#     execute_search(browser, abstract, document)
