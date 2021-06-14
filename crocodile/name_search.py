from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (assert_window_title, get_field_value,
                                        timeout)

from crocodile.crocodile_variables import (first_name_search_field_id,
                                           last_name_search_field_id,
                                           name_search_button_id,
                                           name_search_title, name_search_url)
from crocodile.error_handling import check_login_status


def open_name_search(browser, search_name):
    browser.get(name_search_url)
    if not assert_window_title(browser, name_search_title):
        print(f'Browser failed to open document image link for '
              f'{search_name}, please review.')
        # if check_login_status(browser, document):
        #     browser.get(name_search_url)


def locate_search_field(browser, search_name, field_id, type):
    try:
        search_field_present = EC.element_to_be_clickable((By.ID, field_id))
        WebDriverWait(browser, timeout).until(search_field_present)
        search_field = browser.find_element_by_id(field_id)
        return search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} field for '
              f'{search_name}, please review.')


def split_search_name(search_name):
    pass


def clear_first_name_field(browser, search_name):
    while get_field_value(locate_search_field(browser, search_name, first_name_search_field_id, "first name")) != '':
        locate_search_field(browser, search_name, first_name_search_field_id, "first name").clear()


def enter_first_name(browser, search_name, first_name):
    pass


def handle_first_name_field(browser, search_name, first_name):
    pass


def clear_last_name_field(browser, search_name):
    while get_field_value(locate_search_field(browser, search_name, last_name_search_field_id, "last name")) != '':
        locate_search_field(browser, search_name, last_name_search_field_id, "last name").clear()


def enter_last_name(browser, search_name, last_name):
    pass


def handle_last_name_field(browser, search_name, last_name):
    pass


def enter_search_name(browser, search_name):
    pass


def locate_search_button(browser):
    pass


def execute_search(browser):
    search_button = locate_search_button(browser)
    search_button.click()


def name_search(browser, search_name):
    open_name_search(browser, search_name)
    enter_search_name(browser, search_name)
    execute_search(browser, search_name)
