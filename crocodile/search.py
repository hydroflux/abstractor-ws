from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import assert_window_title, timeout

from crocodile.crocodile_variables import (document_search_title,
                                           document_search_field_id,
                                           search_button_id, search_url)
from crocodile.error_handling import check_login_status


def open_document_search(browser, document):
    browser.get(search_url)
    if not assert_window_title(browser, document_search_title):
        print(f'Browser failed to open document image link for '
              f'{extrapolate_document_value(document)}, please review.')
        if check_login_status(browser, document):
            browser.get(search_url)


def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to fill document field for document number '
              f'{extrapolate_document_value(document)}.')


def get_field_value(field):
    return field.get_attribute("value").strip()


# def check_document_search_field(document_search_field, document):
#     search_field_value = get_field_value(document_search_field)
#     if search_field_value == document_value(document):
#         return True
#     else:
#         return False


def clear_document_search_field(document_search_field):
    while get_field_value(document_search_field) != '':
        document_search_field.clear()


def enter_document_number(document_search_field, document):
    while get_field_value(document_search_field) != document_value(document):
        print(f'Entering document value for '
              f'{extrapolate_document_value(document)}.')
        document_search_field.send_keys(document_value(document))


def handle_document_search_field(browser, document):
    document_search_field = locate_document_search_field(browser, document)
    clear_document_search_field(document_search_field)
    enter_document_number(document_search_field, document)


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
    open_document_search(browser, document)
    handle_document_search_field(browser, document)
    # May need to add additional flag here---
    # need to make sure that the search field is caught properly
    enter_document_number(browser, document)
    execute_search(browser)


def search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        input()
