from selenium.common.exceptions import StaleElementReferenceException

from project_management.timers import naptime

from selenium_utilities.element_interaction import get_parent_element, is_active_class
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (book_and_page_search_button_id,
                                               book_and_page_search_tab_id,
                                               book_search_id,
                                               document_search_button_id,
                                               document_search_field_id,
                                               document_search_tab_id,
                                               page_search_id,
                                               search_navigation_id,
                                               search_script, search_title)

from settings.general_functions import javascript_script_execution, scroll_into_view

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


def wait_for_active(browser, element):
    try:
        return is_active_class(element)
    except StaleElementReferenceException:
        print('Encountered a stale element reference exception '
              'trying to access element class, trying again.')


def access_search_navigation_tab(browser, document):
    return access_element(browser, get_search_navigation_tab, document, "search navigation")


def open_search(browser, document):
    javascript_script_execution(browser, search_script)
    navigation_tab = access_search_navigation_tab(browser, document)
    while not wait_for_active(browser, navigation_tab):
        print("Navigation tab not active, attempting to connect again.")
        naptime()  # Allows time for navigation to load
        navigation_tab = access_search_navigation_tab(browser, document)
    assert search_title


def open_tab(browser, access_function, document):
    tab = access_element(browser, access_function, document, "search tab")
    while not wait_for_active(browser, tab):
        tab = access_element(browser, access_function, document, "search tab")
        tab.click()


def check_for_browser_error(browser):
    if browser.title == "Error":
        print("Browser encountered an error during the search, refreshing the page to attempt to fix the problem.")
        # Review after hitting this error again, browser needs to still be logged in during error to see if this works
        browser.refresh()


def access_document_search_tab(browser, document):
    document_search_tab = get_parent_element(locate_element_by_id(browser, document_search_tab_id,
                                                                  "document search tab", True, document))
    while document_search_tab is None:
        check_for_browser_error(browser)
        document_search_tab = get_parent_element(locate_element_by_id(browser, document_search_tab_id,
                                                                      "document search tab", True, document))
    return document_search_tab


def enter_key_value(browser, field, value):
    scroll_into_view(browser, field)
    field.clear()
    field.send_keys(value)


def enter_document_number(browser, document):
    document_search_field = locate_element_by_id(browser, document_search_field_id,
                                                 "document search field", True, document)
    while document_search_field is None:
        document_search_field = locate_element_by_id(browser, document_search_field_id,
                                                     "document search field", True, document)
    enter_key_value(browser, document_search_field, document.document_value())


def access_book_and_page_search_tab(browser, document):
    book_and_page_search_tab = get_parent_element(locate_element_by_id(browser, book_and_page_search_tab_id,
                                                                       "book and page search tab", True, document))
    while book_and_page_search_tab is None:
        check_for_browser_error(browser)
        book_and_page_search_tab = get_parent_element(locate_element_by_id(browser, book_and_page_search_tab_id,
                                                                           "book and page search tab", True, document))
    return book_and_page_search_tab


def execute_document_number_search(browser, document):
    open_tab(browser, access_document_search_tab, document)
    enter_document_number(browser, document)
    click_button(browser, locate_element_by_id, document_search_button_id,
                 "document search button", document)  # Execute Search


def execute_book_and_page_search(browser, document):
    open_tab(browser, access_book_and_page_search_tab, document)
    book, page = document.document_value()
    # Need to clear the inputs first
    enter_input_value(browser, locate_element_by_id, book_search_id, "book search field", book, document)
    enter_input_value(browser, locate_element_by_id, page_search_id, "page search field", page, document)
    click_button(browser, locate_element_by_id, book_and_page_search_button_id,
                 "book and page search button", document)  # Execute Search


def search(browser, document):
    open_search(browser, document)
    if document.type == "document_number":
        execute_document_number_search(browser, document)
    elif document.type == "book_and_page":
        execute_book_and_page_search(browser, document)
