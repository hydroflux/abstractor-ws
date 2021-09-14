from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value, split_volume_and_page)
from settings.general_functions import get_field_value, timeout

from rattlesnake.rattlesnake_variables import (document_search_field_id,
                                               document_search_url,
                                               page_search_field_id,
                                               search_button_id,
                                               volume_search_field_id)
from rattlesnake.validation import verify_document_search_page_loaded


# This needs to be a loop in order to check against the server error
def open_document_search(browser):
    browser.get(document_search_url)


def locate_search_field(browser, document, id, type):
    try:
        search_field_present = EC.element_to_be_clickable((By.ID, id))
        WebDriverWait(browser, timeout).until(search_field_present)
        search_field = browser.find_element_by_id(id)
        return search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" field for '
              f'{extrapolate_document_value(document)}.')


def clear_document_search_field(browser, document):
    while get_field_value(locate_search_field(browser, document, document_search_field_id, 'reception number')) != '':
        locate_search_field(browser, document, document_search_field_id, 'reception number').clear()


def enter_document_number(browser, document):
    while get_field_value(locate_search_field(browser, document, document_search_field_id, 'reception number')) != \
          document_value(document):
        (locate_search_field(browser, document, document_search_field_id, 'reception number')
         .send_keys(Keys.UP + document_value(document)))


def handle_document_search_field(browser, document):
    clear_document_search_field(browser, document)
    enter_document_number(browser, document)


def clear_volume_search_field(browser, document):
    while get_field_value(locate_search_field(browser, document, volume_search_field_id, 'volume')) != '':
        locate_search_field(browser, document, volume_search_field_id, 'volume').clear()


def enter_volume_number(browser, document, volume):
    while get_field_value(locate_search_field(browser, document, volume_search_field_id, 'volume')) != volume:
        locate_search_field(browser, document, volume_search_field_id, 'volume').send_keys(Keys.UP + volume)


def handle_volume_number_search_field(browser, document, volume):
    clear_volume_search_field(browser, document)
    enter_volume_number(browser, document, volume)


def clear_page_search_field(browser, document):
    while get_field_value(locate_search_field(browser, document, page_search_field_id, 'page')) != '':
        locate_search_field(browser, document, page_search_field_id, 'page').clear()


def enter_page_number(browser, document, page):
    while get_field_value(locate_search_field(browser, document, page_search_field_id, 'page')) != page:
        locate_search_field(browser, document, page_search_field_id, 'page').send_keys(Keys.UP + page)


def handle_page_number_search_field(browser, document, page):
    clear_page_search_field(browser, document)
    enter_page_number(browser, document, page)


def handle_volume_page_search_fields(browser, document):
    volume, page = split_volume_and_page(document)
    handle_volume_number_search_field(browser, document, volume)
    handle_page_number_search_field(browser, document, page)


def locate_search_button(browser, document):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        return search_button
    except TimeoutException:
        print(f'Browser failed to locate search button for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def execute_search(browser, document):
    search_button = locate_search_button(browser, document)
    search_button.click()


def document_search(browser, document):
    handle_document_search_field(browser, document)
    execute_search(browser, document)


def volume_and_page_search(browser, document):
    handle_volume_page_search_fields(browser, document)
    execute_search(browser, document)


def search(browser, document):
    open_document_search(browser)
    verify_document_search_page_loaded(browser, document, open_document_search)
    if document_type(document) == 'document_number':
        document_search(browser, document)
    elif document_type(document) == 'volume_and_page':
        volume_and_page_search(browser, document)
    else:
        print(f'Unable to search document type "{document_type(document)}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()
