from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import assert_window_title, timeout

from crocodile.crocodile_variables import (instrument_search_field_id,
                                           search_button_id, document_search_title,
                                           search_url)


def open_document_search(browser):
    browser.get(search_url)
    assert_window_title(browser, document_search_title)


def locate_document_number_field(browser, document):
    try:
        instrument_search_field_present = EC.presence_of_element_located((By.ID, instrument_search_field_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_field_id)
        return instrument_search_field
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for document number '
              f'{extrapolate_document_value(document)}.')


def enter_document_number(browser, document):
    instrument_search_field = locate_document_number_field(browser, document)
    instrument_search_field.clear()
    instrument_search_field.send_keys(document_value(document))


def locate_search_button(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        return search_button
    except TimeoutException:
        print("Browser timed out trying to locate search button.")


def execute_search(browser):
    search_button = locate_search_button(browser)
    search_button.click()


def document_search(browser, document):
    open_document_search(browser)
    # May need to add additional flag here---
    # need to make sure that the search field is caught properly
    enter_document_number(browser, document)
    execute_search(browser)


def search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')