from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
from settings.general_functions import (check_active_class, get_parent_element,
                                        javascript_script_execution,
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

# Script is nearly identical to tiger search


def locate_search_navigation(browser):
    try:
        search_navigation_present = EC.element_to_be_clickable((By.ID, search_navigation_id))
        WebDriverWait(browser, timeout).until(search_navigation_present)
        search_navigation = browser.find_element_by_id(search_navigation_id)
        return search_navigation
    except TimeoutException:
        print("Browser timed out while trying to open the search navigation.")


def open_search(browser):
    search_navigation = locate_search_navigation(browser)
    while not check_active_class(search_navigation):
        javascript_script_execution(browser, search_script)
        search_navigation = locate_search_navigation(browser)
    assert search_title


def locate_document_search_tab(browser):
    try:
        document_search_tab_present = EC.element_to_be_clickable((By.ID, document_search_tab_id))
        WebDriverWait(browser, timeout).until(document_search_tab_present)
        document_search_tab = browser.find_element_by_id(document_search_tab_id)
        return document_search_tab
    except TimeoutException:
        print("Browser timed out while trying to access the document search tab.")


def open_tab(browser, tab):
    while not check_active_class(get_parent_element(tab)):
        tab.click()


def open_document_search_tab(browser):
    document_search_tab = locate_document_search_tab(browser)
    print("2", document_search_tab)
    open_tab(browser, document_search_tab)


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


def open_book_and_page_search_tab(browser):
    book_and_page_search_tab = locate_document_search_tab(browser)
    open_tab(browser, book_and_page_search_tab)


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
