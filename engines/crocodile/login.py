from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.open import assert_window_title

from settings.county_variables.crocodile import (credentials, post_login_title,
                                                 submit_button_id, website,
                                                 website_title)
from settings.general_functions import enter_field_information, timeout


def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


def locate_login_field(browser, prompt_id, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.ID, prompt_id))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_id(prompt_id)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} prompt, please review.')


def submit_username(browser):
    username_field = locate_login_field(browser, credentials[0], "username")
    enter_field_information(username_field, credentials[2])


def submit_password(browser):
    password_field = locate_login_field(browser, credentials[1], "password")
    enter_field_information(password_field, credentials[3])


def locate_submit_button(browser):
    try:
        submit_button_present = EC.element_to_be_clickable((By.ID, submit_button_id))
        WebDriverWait(browser, timeout).until(submit_button_present)
        submit_button = browser.find_element_by_id(submit_button_id)
        return submit_button
    except TimeoutException:
        print('Browser timed out trying to locate submit button, please review.')


def execute_login(browser):
    submit_button = locate_submit_button(browser)
    submit_button.click()


def verify_login(browser):
    if browser.title == post_login_title:
        print('\nLogin successful, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def account_login(browser):
    open_site(browser)
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)
    verify_login(browser)
