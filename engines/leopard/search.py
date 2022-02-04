from selenium.common.exceptions import StaleElementReferenceException
from engines.leopard.error_handling import check_for_browser_error

from project_management.timers import naptime

from selenium_utilities.element_interaction import get_parent_element, is_active_class
from selenium_utilities.inputs import clear_input, click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (book_and_page_search_button_id,
                                               book_and_page_search_tab_id,
                                               book_search_field_id,
                                               document_search_button_id,
                                               document_search_field_id,
                                               document_search_tab_id,
                                               page_search_field_id,
                                               search_navigation_id,
                                               search_script, search_title)

from settings.general_functions import javascript_script_execution

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


def get_search_navigation_tab(browser, document):
    search_navigation_tab = locate_element_by_id(browser, search_navigation_id, "search navigation",
                                                 True, document)
    while search_navigation_tab is None:
        search_navigation_tab = locate_element_by_id(browser, search_navigation_id, "search navigation",
                                                     True, document)
    return search_navigation_tab


# Can be extrapolated into "selenium_functions" once the script is created
def access_element(browser, access_function, document, element_type):
    try:
        element = access_function(browser, document)
        print("element", element)
        return element
    except StaleElementReferenceException:
        print(f'Encountered a stale element reference exception '
              f'attempting to access {element_type} for '
              f'{document.extrapolate_value()}, please review...')


def access_search_navigation_tab(browser, document):
    return access_element(browser, get_search_navigation_tab, document, "search navigation")


def open_search(browser, document):
    javascript_script_execution(browser, search_script)
    navigation_tab = access_search_navigation_tab(browser, document)
    while not is_active_class(navigation_tab):
        print("Navigation tab not active, attempting to connect again.")
        naptime()  # Allows time for navigation to load
        navigation_tab = access_search_navigation_tab(browser, document)
    assert search_title


def open_tab(browser, document, access_function):
    tab = access_element(browser, access_function, document, "search tab")
    while not is_active_class(tab):
        tab = access_element(browser, access_function, document, "search tab")
        tab.click()


def access_search_type_tab(browser, document, attribute, type):
    search_type_tab = get_parent_element(
        locate_element_by_id(browser, attribute, type, True, document)
    )
    while search_type_tab is None:
        check_for_browser_error(browser)
        search_type_tab = get_parent_element(
            locate_element_by_id(browser, attribute, type, True, document)
        )
    return search_type_tab


def execute_document_number_search(browser, document):
    open_tab(
        browser,
        document,
        access_search_type_tab(attribute=document_search_tab_id, type="document search tab")
    )
    # dropped a 'scroll_into_view' before entering inputs => update the 'enter_input_value' function accordingly
    enter_input_value(
        browser,
        locate_element_by_id,
        document_search_field_id,
        "document search field",
        document.document_value()
    )
    click_button(  # Execute Search
        browser,
        locate_element_by_id,
        document_search_button_id,
        "document search button",
        document
    )


def execute_book_and_page_search(browser, document):
    open_tab(
        browser,
        document,
        access_search_type_tab(attribute=book_and_page_search_tab_id, type="book and page search tab")
    )
    book, page = document.document_value()
    # dropped a 'scroll_into_view' before entering inputs => update the 'enter_input_value' function accordingly
    enter_input_value(browser, locate_element_by_id, book_search_field_id, "book search field", book, document)
    enter_input_value(browser, locate_element_by_id, page_search_field_id, "page search field", page, document)
    click_button(browser, locate_element_by_id, book_and_page_search_button_id,
                 "book and page search button", document)  # Execute Search


def search(browser, document):
    open_search(browser, document)
    if document.type == "document_number":
        clear_input(browser, locate_element_by_id, document_search_field_id, "document search field", document)
        execute_document_number_search(browser, document)
    elif document.type == "book_and_page":
        clear_input(browser, locate_element_by_id, book_search_field_id, "book search field", document)
        clear_input(browser, locate_element_by_id, page_search_field_id, "page search field", document)
        execute_book_and_page_search(browser, document)
