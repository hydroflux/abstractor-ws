from selenium_utilities.locators import locate_element_by_name
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import (assert_window_title, fill_search_field,
                                        naptime, timeout)

from rattlesnake.rattlesnake_variables import (credentials, home_page_title,
                                               home_page_url, login_title,
                                               login_url)
from rattlesnake.validation import verify_login


# Identical to buffalo & armadillo open_site
def open_site(browser):
    browser.get(home_page_url)
    if not assert_window_title(browser, home_page_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


def open_login_prompt(browser):
    browser.get(login_url)
    if not assert_window_title(browser, login_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


# Identical to buffalo & armadillo locate_login_prompt
def locate_login_input(browser, input_name, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.NAME, input_name))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_name(input_name)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} input, please review.')


# Matches buffalo & armadillo submit username
def submit_username(browser):
    fill_search_field(
        locate_login_input(browser, credentials[0], "username"),
        credentials[1])


# Matches buffalo & armadillo submit_password
def submit_password(browser):
    fill_search_field(
        locate_login_input(browser, credentials[2], "password"),
        credentials[3])


def execute_login(browser):
    naptime()
    submit_button = locate_login_input(browser, credentials[4], 'submit')
    submit_button.click()


# Matches the armadillo account_login function
def account_login(browser):
    open_site(browser)
    open_login_prompt(browser)
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)
    verify_login(browser, account_login)
