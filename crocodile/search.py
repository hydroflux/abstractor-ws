from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.inputs import get_field_value
from selenium_utilities.open import assert_window_title

from settings.county_variables.crocodile import (document_search_button_id,
                                                 document_search_field_id,
                                                 document_search_title,
                                                 document_search_url)
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import timeout

from crocodile.error_handling import check_login_status


def open_document_search(browser, document):
    browser.get(document_search_url)
    if not assert_window_title(browser, document_search_title):
        print(f'Browser failed to open document search link for '
              f'{extrapolate_document_value(document)}, please review.')
        if check_login_status(browser, document):
            browser.get(document_search_url)


def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate document field for '
              f'{extrapolate_document_value(document)}.')


def clear_document_search_field(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != '':
        locate_document_search_field(browser, document).clear()


def enter_document_number(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != document_value(document):
        # print(f'Entering document value for '
        #       f'{extrapolate_document_value(document)}.')
        locate_document_search_field(browser, document).send_keys(Keys.UP + document_value(document))


def handle_document_search_field(browser, document):
    clear_document_search_field(browser, document)
    enter_document_number(browser, document)


def locate_search_button(browser, document):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, document_search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(document_search_button_id)
        return search_button
    except TimeoutException:
        print(f'Browser timed out trying to locate search button for '
              f'{extrapolate_document_value(document)}, please review.')


def execute_search(browser, document):
    search_button = locate_search_button(browser, document)
    search_button.click()


def document_search(browser, document):
    open_document_search(browser, document)
    handle_document_search_field(browser, document)
    # May need to add additional flag here---
    # need to make sure that the search field is caught properly
    execute_search(browser, document)


def search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()
