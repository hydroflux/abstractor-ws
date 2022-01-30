from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_utilities.inputs import click_button
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
from settings.file_management import split_book_and_page
from settings.general_functions import (check_active_class, get_parent_element,
                                        javascript_script_execution, naptime,
                                        scroll_into_view, timeout)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)

# Script FUNCTIONALLY is nearly identical to tiger search


def locate_search_navigation(browser, document):
    try:
        search_navigation_present = EC.element_to_be_clickable((By.ID, search_navigation_id))
        WebDriverWait(browser, timeout).until(search_navigation_present)
        search_navigation = browser.find_element_by_id(search_navigation_id)
        return search_navigation
    except TimeoutException:
        print(f'Browser timed out trying to open the search navigation for '
              f'{document.extrapolate_value()}, please review....')
    except StaleElementReferenceException:
        print(f'Encountered a stale element reference exception '
              f'locating search navigation for '
              f'{document.extrapolate_value()}, please review....')


def get_search_navigation_tab(browser, document):
    search_navigation_tab = locate_search_navigation(browser, document)
    while search_navigation_tab is None:
        search_navigation_tab = locate_search_navigation(browser, document)
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
        return check_active_class(element)
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


def locate_document_search_tab(browser, document):
    try:
        document_search_tab_present = EC.element_to_be_clickable((By.ID, document_search_tab_id))
        WebDriverWait(browser, timeout).until(document_search_tab_present)
        document_search_tab = browser.find_element_by_id(document_search_tab_id)
        return document_search_tab
    except TimeoutException:
        print(f'Browser timed out trying to access the document search tab for '
              f'{document.extrapolate_value()}, please review...')
        check_for_browser_error(browser)


def get_document_search_tab(browser, document):
    document_search_tab = get_parent_element(locate_document_search_tab(browser, document))
    while document_search_tab is None:
        document_search_tab = get_parent_element(locate_document_search_tab(browser, document))
    return document_search_tab


def enter_key_value(browser, field, value):
    scroll_into_view(browser, field)
    field.clear()
    field.send_keys(value)


def enter_document_number(browser, document):
    # document_search_field = access_element(browser, locate_document_search_field, document, "document search field")
    document_search_field = locate_element_by_id(browser, document_search_field_id,
                                                 "document search field", True, document)
    while document_search_field is None:
        # document_search_field = access_element(browser,locate_document_search_field,document,"document search field")
        document_search_field = locate_element_by_id(browser, document_search_field_id,
                                                     "document search field", True, document)
        open_tab(browser, get_document_search_tab, document)
    enter_key_value(browser, document_search_field, document.document_value())


def locate_book_and_page_search_tab(browser, document):
    try:
        book_and_page_search_tab_present = EC.element_to_be_clickable((By.ID, book_and_page_search_tab_id))
        WebDriverWait(browser, timeout).until(book_and_page_search_tab_present)
        book_and_page_search_tab = browser.find_element_by_id(book_and_page_search_tab_id)
        return book_and_page_search_tab
    except TimeoutException:
        print(f'Browser timed out trying to access the book and page search tab for '
              f'{document.extrapolate_value()}, please review....')


def get_book_and_page_search_tab(browser, document):
    book_and_page_search_tab = get_parent_element(locate_book_and_page_search_tab(browser, document))
    while book_and_page_search_tab is None:
        book_and_page_search_tab = get_parent_element(locate_book_and_page_search_tab(browser, document))
    return book_and_page_search_tab


def enter_book_number(browser, document, book):
    # book_search_field = access_element(browser, locate_book_search_field, document, "book field")
    book_search_field = locate_element_by_id(browser, book_search_id, "book search field", True, document)
    while book_search_field is None:
        # book_search_field = access_element(browser, locate_book_search_field, document, "book field")
        book_search_field = locate_element_by_id(browser, book_search_id, "book search field", True, document)
        open_tab(browser, get_book_and_page_search_tab, document)
    enter_key_value(browser, book_search_field, book)


def enter_page_number(browser, document, page):
    # page_search_field = access_element(browser, locate_page_search_field, "page field")
    page_search_field = locate_element_by_id(browser, page_search_id, "page search field", True, document)
    while page_search_field is None:
        # page_search_field = access_element(browser, locate_page_search_field, "page field")
        page_search_field = locate_element_by_id(browser, page_search_id, "page search field", True, document)
        open_tab(browser, get_book_and_page_search_tab, document)
    enter_key_value(browser, page_search_field, page)


def execute_document_number_search(browser, document):
    open_tab(browser, get_document_search_tab, document)
    enter_document_number(browser, document)
    click_button(browser, locate_element_by_id, document_search_button_id,
                 "document search button", document)  # Execute Search


def execute_book_and_page_search(browser, document):
    open_tab(browser, get_book_and_page_search_tab, document)
    book, page = split_book_and_page(document)
    enter_book_number(browser, document, book)
    enter_page_number(browser, document, page)
    click_button(browser, locate_element_by_id, book_and_page_search_button_id,
                 "book and page search button", document)  # Execute Search


def search(browser, document):
    open_search(browser, document)
    if document.type == "document_number":
        execute_document_number_search(browser, document)
    elif document.type == "book_and_page":
        execute_book_and_page_search(browser, document)
