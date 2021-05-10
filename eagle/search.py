from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
from settings.general_functions import (medium_nap, naptime, scroll_into_view,
                                        timeout)

from eagle.eagle_variables import (book_search_id, clear_search_id,
                                   instrument_search_id, page_search_id,
                                   search_button_id, search_title, search_url)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


def open_search(browser):
    browser.get(search_url)
    assert search_title


def get_clear_search_button(browser):
    try:
        clear_search_button_present = EC.presence_of_element_located((By.ID, clear_search_id))
        WebDriverWait(browser, timeout).until(clear_search_button_present)
        clear_search_button = browser.find_element_by_id(clear_search_id)
        return clear_search_button
    except TimeoutException:
        print("Browser timed out while trying to clear the search form.")


def execute_clear_search(browser, button):
    try:
        scroll_into_view(browser, button)
        button.click()
        return True
    except ElementClickInterceptedException:
        print("Encountered an element click interception exception while trying to clear the search form, refreshing & trying again.")
        return False


def clear_search(browser):
    clear = False
    while clear is not True:
        clear_search_button = get_clear_search_button(browser)
        clear = execute_clear_search(browser, clear_search_button)
        if clear is False:
            browser.refresh()
            medium_nap()


def enter_document_number(browser, document):
    try:
        instrument_search_field_present = EC.presence_of_element_located((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        instrument_search_field.clear()
        instrument_search_field.send_keys(document_value(document))
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for document number '
              f'{extrapolate_document_value(document)}.')


def enter_book_number(browser, book):
    try:
        book_search_field_present = EC.presence_of_element_located((By.ID, book_search_id))
        WebDriverWait(browser, timeout).until(book_search_field_present)
        book_search_field = browser.find_element_by_id(book_search_id)
        book_search_field.clear()
        book_search_field.send_keys(book)
        return True
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for Book: {book}.')
        return False


def enter_page_number(browser, page):
    try:
        page_search_field_present = EC.presence_of_element_located((By.ID, page_search_id))
        WebDriverWait(browser, timeout).until(page_search_field_present)
        page_search_field = browser.find_element_by_id(page_search_id)
        page_search_field.clear()
        page_search_field.send_keys(page)
        return True
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for Page: {page}.')
        return False


def prepare_book_and_page_search(browser, document):
    book, page = split_book_and_page(document)
    ready = False
    while not ready:
        if enter_book_number(browser, book) and enter_page_number(browser, page):
            ready = True
        else:
            open_search(browser)


def execute_search(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        scroll_into_view(browser, search_button)
        search_button.click()
    except TimeoutException:
        print("Browser timed out while trying to execute search.")


def document_search(browser, document):
    open_search(browser)
    clear_search(browser)
    naptime() # Consider testing without this nap to see if necessary
    if document_type(document) == "document_number":
        enter_document_number(browser, document)
    elif document_type(document) == "book_and_page":
        prepare_book_and_page_search(browser, document)
    execute_search(browser)
