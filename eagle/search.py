from selenium.common.exceptions import (ElementClickInterceptedException, JavascriptException,
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
from eagle.error_handling import check_for_error
from eagle.login import check_login_status

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


def open_search(browser):
    browser.get(search_url)
    check_login_status(browser)  # Try here, if unsuccessful move to after open_search
    assert search_title


def get_clear_search_button(browser, document):
    try:
        clear_search_button_present = EC.presence_of_element_located((By.ID, clear_search_id))
        WebDriverWait(browser, timeout).until(clear_search_button_present)
        clear_search_button = browser.find_element_by_id(clear_search_id)
        return clear_search_button
    except TimeoutException:
        print("Browser timed out trying to clear the search form.")
        check_for_error(browser, document)


def execute_clear_search(browser, button):
    try:
        scroll_into_view(browser, button)
        button.click()
        return True
    except ElementClickInterceptedException:
        print('Encountered an element click interception exception trying to clear the search form, '
              'refreshing & trying again.')
        return False
    except JavascriptException:
        print('Encountered an javascript exception trying to clear the search form, '
              'refreshing & trying again.')
        return False


def clear_search(browser, document):
    clear = False
    while clear is not True:
        clear_search_button = get_clear_search_button(browser, document)
        clear = execute_clear_search(browser, clear_search_button)
        if clear is False:
            # browser.refresh()  #  Commented out on June 22, 2021
            # medium_nap()  #  Commented out on June 22, 2021
            browser.back()  # Should work for JS exceptions--don't know about Element Click Interceptions
            medium_nap()
            open_search(browser)


def locate_document_number_field(browser, document):
    try:
        instrument_search_field_present = EC.presence_of_element_located((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        return instrument_search_field
    except TimeoutException:
        print(f'Browser timed out trying to fill document field for document number '
              f'{extrapolate_document_value(document)}.')


def handle_document_number_field(browser, document):
    instrument_search_field = locate_document_number_field(browser, document)
    while type(instrument_search_field) is None:
        check_for_error(browser, document)
        instrument_search_field = locate_document_number_field(browser, document)


def enter_document_number(browser, document):
    instrument_search_field = handle_document_number_field(browser, document)
    instrument_search_field.clear()
    instrument_search_field.send_keys(document_value(document))


def enter_book_number(browser, book):
    try:
        book_search_field_present = EC.presence_of_element_located((By.ID, book_search_id))
        WebDriverWait(browser, timeout).until(book_search_field_present)
        book_search_field = browser.find_element_by_id(book_search_id)
        book_search_field.clear()
        book_search_field.send_keys(book)
        return True
    except TimeoutException:
        print(f'Browser timed out trying to fill document field for Book: {book}.')
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
        print(f'Browser timed out trying to fill document field for Page: {page}.')
        return False


def prepare_book_and_page_search(browser, document):
    book, page = split_book_and_page(document)
    ready = False
    while not ready:
        if enter_book_number(browser, book) and enter_page_number(browser, page):
            ready = True
        else:
            open_search(browser)


def locate_search_button(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        return search_button
    except TimeoutException:
        print("Browser timed out trying to execute search.")


def execute_search(browser):
    search_button = locate_search_button(browser)
    scroll_into_view(browser, search_button)
    search_button.click()


def document_search(browser, document):
    open_search(browser)
    clear_search(browser, document)
    naptime()  # Consider testing without this nap to see if necessary
    if document_type(document) == "document_number":
        enter_document_number(browser, document)
    elif document_type(document) == "book_and_page":
        prepare_book_and_page_search(browser, document)
    execute_search(browser)
