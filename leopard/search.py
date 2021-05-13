from leopard.record import get_document_content
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
from settings.general_functions import (check_active_class, get_parent_element,
                                        javascript_script_execution, short_nap,
                                        scroll_into_view, timeout)

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


def locate_search_navigation(browser):
    try:
        search_navigation_present = EC.element_to_be_clickable((By.ID, search_navigation_id))
        WebDriverWait(browser, timeout).until(search_navigation_present)
        search_navigation = browser.find_element_by_id(search_navigation_id)
        return search_navigation
    except TimeoutException:
        print("Browser timed out while trying to open the search navigation.")
    except StaleElementReferenceException:
        print("Encountered a stale element reference exception while locating search navigation, trying again.")


def get_search_navigation_tab(browser):
    search_navigation_tab = locate_search_navigation(browser)
    while search_navigation_tab is None:
        search_navigation_tab = locate_search_navigation(browser)
    return search_navigation_tab


def access_element(browser, access_function):
    try:
        element = access_function(browser)
        return check_active_class(element)
    except StaleElementReferenceException:
        print('Encountered a stale element reference exception '
              'while trying to access element class.')


# If it continues to work like this the reason that it's getting slowing is because
# it's checking before the element has time to populate--it's just checking too fast
# The fact that it broke where it did means this IS NOT always the case


def open_search(browser):
    javascript_script_execution(browser, search_script)
    # search_navigation = access_search_navigation(browser)
    # while not check_active_class(search_navigation):
    while not access_element(browser, get_search_navigation_tab):
        javascript_script_execution(browser, search_script)
        short_nap()
        # search_navigation = access_search_navigation(browser)
    assert search_title


def locate_document_search_tab(browser):
    try:
        document_search_tab_present = EC.element_to_be_clickable((By.ID, document_search_tab_id))
        WebDriverWait(browser, timeout).until(document_search_tab_present)
        document_search_tab = browser.find_element_by_id(document_search_tab_id)
        return document_search_tab
    except TimeoutException:
        print("Browser timed out while trying to access the document search tab.")


def get_document_search_tab(browser):
    document_search_tab = get_parent_element(locate_document_search_tab(browser))
    while document_search_tab is None:
        document_search_tab = get_parent_element(locate_document_search_tab(browser))
    return document_search_tab


def open_tab(browser, access_tab_function):
    while not access_element(browser, access_tab_function):
        tab = access_tab_function(browser)
        tab.click()


def open_document_search_tab(browser):
    # document_search_tab = get_document_search_tab(browser)
    open_tab(browser, get_document_search_tab)


def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out while trying to locate document number field for '
              f'{extrapolate_document_value(document)}.')


def enter_key_value(browser, field, value):
    scroll_into_view(browser, field)
    field.clear()
    field.send_keys(value)


def enter_document_number(browser, document):
    document_search_field = locate_document_search_field(browser, document)
    enter_key_value(browser, document_search_field, document_value(document))


def locate_book_and_page_search_tab(browser):
    try:
        book_and_page_search_tab_present = EC.element_to_be_clickable((By.ID, book_and_page_search_tab_id))
        WebDriverWait(browser, timeout).until(book_and_page_search_tab_present)
        book_and_page_search_tab = browser.find_element_by_id(book_and_page_search_tab_id)
        return book_and_page_search_tab
    except TimeoutException:
        print("Browser timed out while trying to access the book and page search tab.")


def get_book_and_page_search_tab(browser):
    book_and_page_search_tab = locate_book_and_page_search_tab(browser)
    while book_and_page_search_tab is None:
        book_and_page_search_tab = locate_book_and_page_search_tab(browser)
    return book_and_page_search_tab


def open_book_and_page_search_tab(browser):
    open_tab(browser, get_book_and_page_search_tab)


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
    book_search_field = locate_book_search_field(browser, document)
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
    page_search_field = locate_page_search_field(browser, document)
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
    open_document_search_tab(browser)
    enter_document_number(browser, document)
    execute_search(browser, document, document_search_button_id)


def execute_book_and_page_search(browser, document):
    open_book_and_page_search_tab(browser)
    book, page = split_book_and_page(document)
    enter_book_number(browser, document, book)
    enter_page_number(browser, document, page)
    execute_search(browser, document, book_and_page_search_button_id)


def search(browser, document):
    open_search(browser)
    if document_type(document) == "document_number":
        execute_document_number_search(browser, document)
    elif document_type(document) == "book_and_page":
        execute_book_and_page_search(browser, document)
