from engines.leopard.error_handling import check_for_browser_error

from project_management.timers import naptime

from selenium_utilities.element_interaction import get_parent_element, is_active_class
from selenium_utilities.inputs import clear_input, click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_id

from settings.general_functions import javascript_script_execution

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


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


def search(browser, abstract, document):
    open_search(browser, abstract, document)
    open_search_type_tab(browser, abstract, document)
    clear_search(browser, abstract, document)
    enter_input(browser, abstract, document)
    execute_search(browser, abstract, document)
