from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import (document_value,
                                      extrapolate_document_value,
                                      split_volume_and_page)
from settings.general_functions import get_field_value, timeout

from rattlesnake.rattlesnake_variables import (document_search_field_id,
                                               document_search_url,
                                               page_search_field_id,
                                               search_button_id,
                                               volume_search_field_id)
from rattlesnake.validation import verify_document_search_page_loaded


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


def clear_search_field(browser, document, type, id):
    while get_field_value(locate_search_field(browser, document, id, type)) != '':
        locate_search_field(browser, document, id, type).clear()


def enter_value_number(browser, document, type, id, value):
    while get_field_value(locate_search_field(browser, document, id, type)) != value:
        locate_search_field(browser, document, id, type).send_keys(Keys.UP + value)


def handle_document_search_field(browser, document, type="reception number", id=document_search_field_id):
    value = document_value(document)
    clear_search_field(browser, document, type, id)
    enter_value_number(browser, document, type, id, value)


def handle_volume_number_search_field(browser, document, volume, type="volume", id=volume_search_field_id):
    clear_search_field(browser, document, type, id)
    enter_value_number(browser, document, type, id, volume)


def handle_page_number_search_field(browser, document, page, type="page", id=page_search_field_id):
    clear_search_field(browser, document, type, id)
    enter_value_number(browser, document, type, id, page)


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
    if document.type == 'document_number':
        document_search(browser, document)
    elif document.type == 'volume_and_page':
        volume_and_page_search(browser, document)
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()
