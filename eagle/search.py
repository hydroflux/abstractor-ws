from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)

from settings.general_functions import naptime
from settings.settings import timeout
from settings.file_management import document_type

from eagle.eagle_variables import (book_search_id, clear_search_id,
                                   instrument_search_id, page_search_id,
                                   search_button_id, search_title, search_url)


def open_search(browser):
    browser.get(search_url)
    assert search_title


def clear_search(browser):
    try:
        clear_search_present = EC.presence_of_element_located((By.ID, clear_search_id))
        WebDriverWait(browser, timeout).until(clear_search_present)
        clear_search = browser.find_element_by_id(clear_search_id)
        browser.execute_script("arguments[0].scrollIntoView();", clear_search)
        clear_search.click()
    except TimeoutException:
        print("Browser timed out while trying to clear the search form.")


def enter_document_number(browser, document_number):
    try:
        instrument_search_field_present = EC.presence_of_element_located((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        instrument_search_field.clear()
        instrument_search_field.send_keys(document_number.value)
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for document number {document_number.value}.')


def split_book_and_page(book_and_page):
    book = book_and_page.value["Book"]
    page = book_and_page.value["Page"]
    return book, page


def enter_book_number(browser, book):
    try:
        book_search_field_present = EC.presence_of_element_located((By.ID, book_search_id))
        WebDriverWait(browser, timeout).until(book_search_field_present)
        book_search_field = browser.find_element_by_id(book_search_id)
        book_search_field.clear()
        book_search_field.send_keys(book)
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for B: {book}.')


def enter_page_number(browser, page):
    try:
        page_search_field_present = EC.presence_of_element_located((By.ID, page_search_id))
        WebDriverWait(browser, timeout).until(page_search_field_present)
        page_search_field = browser.find_element_by_id(page_search_id)
        page_search_field.clear()
        page_search_field.send_keys(page)
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for P: {page}.')


def execute_search(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        search_button.click()
    except TimeoutException:
        print("Browser timed out while trying to execute search.")


def document_search(browser, document):
    open_search(browser)
    clear_search(browser)
    naptime()
    if document_type(document) == "document_number":
        enter_document_number(browser, document)
    elif document_type(document) == "book_and_page":
        book, page = split_book_and_page(document)
        enter_book_number(browser, book)
        enter_page_number(browser, page)
    execute_search(browser)
