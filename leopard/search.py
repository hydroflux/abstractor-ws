from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
from settings.general_functions import (check_active_class, get_parent_element,
                                        javascript_script_execution,
                                        scroll_into_view, short_nap, timeout)

from leopard.leopard_variables import (book_and_page_search_button_id,
                                       book_and_page_search_tab_id,
                                       book_search_id,
                                       document_search_button_id,
                                       document_search_field_id,
                                       document_search_tab_id, page_search_id,
                                       search_navigation_id, search_script,
                                       search_title)

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
              f'{extrapolate_document_value(document)}.')
    except StaleElementReferenceException:
        print(f'Encountered a stale element reference exception '
              f'locating search navigation for '
              f'{extrapolate_document_value(document)}.')


def get_search_navigation_tab(browser, document):
    search_navigation_tab = locate_search_navigation(browser, document)
    while search_navigation_tab is None:
        search_navigation_tab = locate_search_navigation(browser, document)
    return search_navigation_tab


# Can be extrapolated into "selenium_functions" once the script is created
def access_element(browser, access_function, document, element_type):
    try:
        return access_function(browser, document)
    except StaleElementReferenceException:
        print(f'Encountered a stale element reference exception '
              f'attempting to access {element_type} for '
              f'{extrapolate_document_value(document)}')


# def wait_for_active(browser, access_function):
#     try:
#         element = access_function(browser)
#         return check_active_class(element)
#     except StaleElementReferenceException:
#         print('Encountered a stale element reference exception '
#               'while trying to access element class.')


def open_search(browser, document):
    javascript_script_execution(browser, search_script)
    search_navigation_tab = access_element(browser, get_search_navigation_tab, document, "search navigation")
    while not check_active_class(search_navigation_tab):
        javascript_script_execution(browser, search_script)
        short_nap()
        search_navigation_tab = access_element(browser, get_search_navigation_tab, document, "search navigation")
    assert search_title


def open_tab(browser, access_function, document):
    tab = access_element(browser, access_function, document, "search tab")
    while not check_active_class(tab):
        tab = access_element(browser, access_function, document, "search tab")
        tab.click()


def locate_document_search_tab(browser, document):
    try:
        document_search_tab_present = EC.element_to_be_clickable((By.ID, document_search_tab_id))
        WebDriverWait(browser, timeout).until(document_search_tab_present)
        document_search_tab = browser.find_element_by_id(document_search_tab_id)
        return document_search_tab
    except TimeoutException:
        print(f'Browser timed out trying to access the document search tab for '
              f'{extrapolate_document_value(document)}')


def get_document_search_tab(browser, document):
    document_search_tab = get_parent_element(locate_document_search_tab(browser, document))
    while document_search_tab is None:
        document_search_tab = get_parent_element(locate_document_search_tab(browser, document))
    return document_search_tab


def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate document number field for '
              f'{extrapolate_document_value(document)}.')


def enter_key_value(browser, field, value):
    scroll_into_view(browser, field)
    field.clear()
    field.send_keys(value)


def enter_document_number(browser, document):
    document_search_field = access_element(browser, locate_document_search_field, document, "document search field")
    while document_search_field is None:
        document_search_field = access_element(browser, locate_document_search_field, document, "document search field")
    enter_key_value(browser, document_search_field, document_value(document))


def locate_book_and_page_search_tab(browser, document):
    try:
        book_and_page_search_tab_present = EC.element_to_be_clickable((By.ID, book_and_page_search_tab_id))
        WebDriverWait(browser, timeout).until(book_and_page_search_tab_present)
        book_and_page_search_tab = browser.find_element_by_id(book_and_page_search_tab_id)
        return book_and_page_search_tab
    except TimeoutException:
        print(f'Browser timed out while trying to access the book and page search tab for '
              f'{extrapolate_document_value(document)}.')


def get_book_and_page_search_tab(browser, document):
    book_and_page_search_tab = get_parent_element(locate_book_and_page_search_tab(browser, document))
    while book_and_page_search_tab is None:
        book_and_page_search_tab = get_parent_element(locate_book_and_page_search_tab(browser, document))
    return book_and_page_search_tab


def locate_book_search_field(browser, document):
    try:
        book_search_field_present = EC.element_to_be_clickable((By.ID, book_search_id))
        WebDriverWait(browser, timeout).until(book_search_field_present)
        book_search_field = browser.find_element_by_id(book_search_id)
        return book_search_field
    except TimeoutException:
        print(f'Browser timed out while trying to locate book field for '
              f'{extrapolate_document_value(document)}.')


def enter_book_number(browser, document, book):
    book_search_field = access_element(browser, locate_book_search_field, document, "book field")
    while book_search_field is None:
        book_search_field = access_element(browser, locate_book_search_field, document, "book field")
    enter_key_value(browser, book_search_field, book)


def locate_page_search_field(browser, document):
    try:
        page_search_field_present = EC.element_to_be_clickable((By.ID, page_search_id))
        WebDriverWait(browser, timeout).until(page_search_field_present)
        page_search_field = browser.find_element_by_id(page_search_id)
        return page_search_field
    except TimeoutException:
        print(f'Browser timed out while trying to locate page field for '
              f'{extrapolate_document_value(document)}.')


def enter_page_number(browser, document, page):
    page_search_field = access_element(browser, locate_page_search_field, "page field")
    while page_search_field is None:
        page_search_field = access_element(browser, locate_page_search_field, "page field")
    enter_key_value(browser, page_search_field, page)


def locate_search_button(browser, document, button_id):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(button_id)
        return search_button
    except TimeoutException:
        print(f'Browser timed out while trying to locate search button for '
              f'{extrapolate_document_value(document)}.')


def execute_search(browser, document, button_id):
    search_button = locate_search_button(browser, document, button_id)
    search_button.click()


def execute_document_number_search(browser, document):
    open_tab(browser, get_document_search_tab, document)
    enter_document_number(browser, document)
    execute_search(browser, document, document_search_button_id)


def execute_book_and_page_search(browser, document):
    open_tab(browser, get_book_and_page_search_tab, document)
    book, page = split_book_and_page(document)
    enter_book_number(browser, document, book)
    enter_page_number(browser, document, page)
    execute_search(browser, document, book_and_page_search_button_id)


def search(browser, document):
    open_search(browser, document)
    if document_type(document) == "document_number":
        execute_document_number_search(browser, document)
    elif document_type(document) == "book_and_page":
        execute_book_and_page_search(browser, document)
