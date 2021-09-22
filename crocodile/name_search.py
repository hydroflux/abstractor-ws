from selenium_utilities.inputs import get_field_value
from selenium_utilities.open import assert_window_title
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from crocodile.crocodile_variables import (first_name_search_field_id,
                                           last_name_search_field_id,
                                           name_search_button_id,
                                           name_search_title, name_search_url)


def open_name_search(browser, search_name):
    browser.get(name_search_url)
    if not assert_window_title(browser, name_search_title):
        print(f'Browser failed to open document image link for '
              f'{search_name.value}, please review.')
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
              f'{search_name.value}, please review.')


def split_search_name(search_name):
    # Obviously this isn't going to work consistently,
    # so it's working as a placeholder for now until it becomes necessary to
    # expand
    return search_name.value.split()


def clear_last_name_field(browser, search_name):
    while get_field_value(locate_search_field(
            browser, search_name, last_name_search_field_id, "last name")) != '':
        locate_search_field(
            browser, search_name, last_name_search_field_id, "last name").clear()


def enter_last_name(browser, search_name, last_name):
    while get_field_value(locate_search_field(
            browser, search_name, last_name_search_field_id, "last name")) != last_name:
        locate_search_field(
            browser, search_name, last_name_search_field_id, "last name").send_keys(Keys.UP + last_name)


def handle_last_name_field(browser, search_name, last_name):
    clear_last_name_field(browser, search_name)
    enter_last_name(browser, search_name, last_name)


def clear_first_name_field(browser, search_name):
    while get_field_value(locate_search_field(browser, search_name, first_name_search_field_id, "first name")) != '':
        locate_search_field(
            browser, search_name, first_name_search_field_id, "first name").clear()


def enter_first_name(browser, search_name, first_name):
    while get_field_value(locate_search_field(
            browser, search_name, first_name_search_field_id, "first name")) != first_name:
        locate_search_field(
            browser, search_name, first_name_search_field_id, "first name").send_keys(Keys.UP + first_name)


def handle_first_name_field(browser, search_name, first_name):
    clear_first_name_field(browser, search_name)
    enter_first_name(browser, search_name, first_name)


def enter_search_name(browser, search_name):
    first_name, last_name = split_search_name(search_name)
    handle_last_name_field(browser, search_name, last_name)
    handle_first_name_field(browser, search_name, first_name)


def locate_name_search_button(browser, search_name):
    try:
        name_search_button_present = EC.element_to_be_clickable((By.ID, name_search_button_id))
        WebDriverWait(browser, timeout).until(name_search_button_present)
        name_search_button = browser.find_element_by_id(name_search_button_id)
        return name_search_button
    except TimeoutException:
        print(f'Browser timed out trying to locate search button performing a name search for '
              f'{search_name.value}, please review.')


def execute_name_search(browser, search_name):
    name_search_button = locate_name_search_button(browser, search_name)
    name_search_button.click()


def search_provided_name(browser, search_name):
    open_name_search(browser, search_name)
    enter_search_name(browser, search_name)
    execute_name_search(browser, search_name)
