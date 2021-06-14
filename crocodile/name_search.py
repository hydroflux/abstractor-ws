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


def locate_last_name_search_field(browser, search_name):
    try:
        last_name_search_field_present = EC.element_to_be_clickable((By.ID, last_name_search_field_id))
        WebDriverWait(browser, timeout).until(last_name_search_field_present)
        last_name_search_field = browser.find_element_by_id(last_name_search_field_id)
        return last_name_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate last name field for '
              f'{search_name}, please review.')


def locate_first_name_search_field(browser, search_name):
    try:
        first_name_search_field_present = EC.element_to_be_clickable((By.ID, first_name_search_field_id))
        WebDriverWait(browser, timeout).until(first_name_search_field_present)
        first_name_search_field = browser.find_element_by_id(first_name_search_field_id)
        return first_name_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate first name field for '
              f'{search_name}, please review.')