from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
from settings.general_functions import (javascript_script_execution,
                                        scroll_into_view, short_nap, get_parent_element, check_active_class, timeout)

from leopard.leopard_variables import (book_and_page_search_button_id,
                                       book_and_page_search_tab_id,
                                       book_search_id,
                                       document_search_button_id,
                                       document_search_tab_id,
                                       instrument_search_id, page_search_id,
                                       search_navigation_id, search_script,
                                       search_title)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)

# Script is nearly identical to tiger search


def open_search(browser):
    try:
        search_navigation_present = EC.element_to_be_clickable((By.ID, search_navigation_id))
        WebDriverWait(browser, timeout).until(search_navigation_present)
        search_navigation = browser.find_element_by_id(search_navigation_id)
        if check_active_class(search_navigation):
            return
        javascript_script_execution(browser, search_script)
        assert search_title
    except TimeoutException:
        print("Browser timed out while trying to open the search navigation.")


def open_document_search_tab(browser):
    try:
        document_search_tab_present = EC.element_to_be_clickable((By.ID, document_search_tab_id))
        WebDriverWait(browser, timeout).until(document_search_tab_present)
        document_search_tab = browser.find_element_by_id(document_search_tab_id)
        scroll_into_view(browser, document_search_tab)
        if check_active_class(get_parent_element(document_search_tab)):
            return
        document_search_tab.click()
        short_nap()
        document_search_tab.click()
    except TimeoutException:
        print("Browser timed out while trying to access the document search tab.")


def open_book_and_page_search_tab(browser):
    try:
        book_and_page_search_tab_present = EC.element_to_be_clickable((By.ID, book_and_page_search_tab_id))
        WebDriverWait(browser, timeout).until(book_and_page_search_tab_present)
        book_and_page_search_tab = browser.find_element_by_id(book_and_page_search_tab_id)
        scroll_into_view(browser, book_and_page_search_tab)
        if check_active_class(get_parent_element(book_and_page_search_tab)):
            return
        book_and_page_search_tab.click()
        short_nap()
        book_and_page_search_tab.click()
    except TimeoutException:
        print("Browser timed out while trying to access the book and page search tab.")


def enter_document_number(browser, document):
    try:
        instrument_search_field_present = EC.element_to_be_clickable((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        instrument_search_field.clear()
        instrument_search_field.send_keys(document_value(document))
    except TimeoutException:
        print(f'Browser timed out while trying to fill document number field for '
              f'{extrapolate_document_value(document)}, trying again.')


def enter_book_number(browser, document, book):
    try:
        book_search_field_present = EC.element_to_be_clickable((By.ID, book_search_id))
        WebDriverWait(browser, timeout).until(book_search_field_present)
        book_search_field = browser.find_element_by_id(book_search_id)
        book_search_field.clear()
        book_search_field.send_keys(book)
    except TimeoutException:
        print(f'Browser timed out while trying to fill book field for '
              f'{extrapolate_document_value(document)}, trying again.')


def enter_page_number(browser, document, page):
    try:
        page_search_field_present = EC.element_to_be_clickable((By.ID, page_search_id))
        WebDriverWait(browser, timeout).until(page_search_field_present)
        page_search_field = browser.find_element_by_id(page_search_id)
        page_search_field.clear()
        page_search_field.send_keys(page)
    except TimeoutException:
        print(f'Browser timed out while trying to fill page field for '
              f'{extrapolate_document_value(document)}, trying again.')


def identify_search_button(document):
    if document_type(document) == "document_number":
        return document_search_button_id
    elif document_type(document) == "book_and_page":
        return book_and_page_search_button_id


def execute_search(browser, document):
    search_button_id = identify_search_button(document)
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        search_button.click()
    except TimeoutException:
        print(f'Browser timed out while trying to execute search for '
              f'{extrapolate_document_value(document)}')


def search(browser, document):
    open_search(browser)
    if document_type(document) == "document_number":
        open_document_search_tab(browser)
        enter_document_number(browser, document)
    elif document_type(document) == "book_and_page":
        open_book_and_page_search_tab(browser)
        book, page = split_book_and_page(document)
        enter_book_number(browser, document, book)
        enter_page_number(browser, document, page)
    execute_search(browser, document)
