from buffalo.frame_handling import switch_to_main_frame, switch_to_search_frame
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_type, extrapolate_document_value
from settings.general_functions import get_field_value, timeout, get_element_class

from buffalo.buffalo_variables import search_page_button_id, document_search_menu_id, search_menu_active_class


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
    switch_to_search_frame(browser)
    handle_document_search_menu(browser, document)


def clear_document_search_field(browser, document):
    pass


def enter_document_number(browser, document):
    pass


def handle_document_search_field(browser, document):
    enter_document_number(browser, document)
    clear_document_search_field(browser, document)


def execute_search(browser, document):
    pass


def document_search(browser, document):
    handle_document_search_field(browser, document)
    execute_search(browser, document)


def search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()
