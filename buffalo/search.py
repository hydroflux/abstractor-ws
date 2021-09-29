from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.county_variables.buffalo import (
    document_search_field_class_name, document_search_menu_id,
    search_input_header_text, search_menu_active_class, search_page_button_id)
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (get_element_class, get_field_value,
                                        timeout)

from buffalo.frame_handling import (switch_to_main_frame,
                                    switch_to_search_input_frame,
                                    switch_to_search_menu_frame)
from buffalo.validation import page_is_loaded


def locate_search_page_button(browser, document):
    try:
        search_page_button_present = EC.element_to_be_clickable((By.ID, search_page_button_id))
        WebDriverWait(browser, timeout).until(search_page_button_present)
        search_page_button = browser.find_element_by_id(search_page_button_id)
        return search_page_button
    except TimeoutException:
        print(f'Browser timed out trying to locate search page button for document '
              f'{extrapolate_document_value(document)}, please review.')


def open_search_page(browser, document):
    browser.refresh()
    switch_to_main_frame(browser)
    search_page_button = locate_search_page_button(browser, document)
    search_page_button.click()


def locate_document_search_menu(browser, document):
    try:
        document_search_menu_present = EC.element_to_be_clickable((By.ID, document_search_menu_id))
        WebDriverWait(browser, timeout).until(document_search_menu_present)
        document_search_menu = browser.find_element_by_id(document_search_menu_id)
        return document_search_menu
    except TimeoutException:
        print(f'Browser timed out trying to locate document search menu for document '
              f'{extrapolate_document_value(document)}, please review.')


def menu_is_active(menu):
    if get_element_class(menu).endswith(search_menu_active_class):
        return True


def handle_document_search_menu(browser, document):
    document_search_menu = locate_document_search_menu(browser, document)
    while not menu_is_active(document_search_menu):
        document_search_menu.click()


def open_document_search_menu(browser, document):
    switch_to_search_menu_frame(browser)
    handle_document_search_menu(browser, document)


def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.presence_of_element_located((
            By.CLASS_NAME, document_search_field_class_name))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_class_name(document_search_field_class_name)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate document field for '
              f'{extrapolate_document_value(document)}.')


def get_document_search_field(browser, document):
    switch_to_search_input_frame(browser)
    return locate_document_search_field(browser, document)


# Nearly identical to crocodile clear_document_search_field
def clear_document_search_field(browser, document):
    while get_field_value(get_document_search_field(browser, document)) != '':
        get_document_search_field(browser, document).clear()


def clear_double_entry(browser, document):
    value = document_value(document)
    if get_field_value(get_document_search_field(browser, document)) == f'{value}{value}':
        clear_document_search_field(browser, document)


def enter_document_number(browser, document):
    while get_field_value(get_document_search_field(browser, document)) != document_value(document):
        clear_double_entry(browser, document)
        get_document_search_field(browser, document).send_keys(Keys.UP + document_value(document))


def execute_search(browser, document):
    get_document_search_field(browser, document).send_keys(Keys.RETURN)


def document_search(browser, document):
    open_document_search_menu(browser, document)
    clear_document_search_field(browser, document)
    enter_document_number(browser, document)
    execute_search(browser, document)


def process_document_search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def search(browser, document):
    open_search_page(browser, document)
    if page_is_loaded(browser, search_input_header_text):
        process_document_search(browser, document)
