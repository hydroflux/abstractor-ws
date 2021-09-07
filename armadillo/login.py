from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import (assert_window_title, fill_search_field,
                                        timeout)

from armadillo.armadillo_variables import (county_site, credentials,
                                           post_login_title, website,
                                           website_title)
from armadillo.validation import validate_login


# Identical to buffalo open_site
def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


# Identical to buffalo open_site
def locate_login_input(browser, input_name, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.NAME, input_name))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_name(input_name)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} input, please review.')


# Matches buffalo submit_password
def submit_username(browser):
    fill_search_field(
        locate_login_input(browser, credentials[0], "username"),
        credentials[1])


# Matches buffalo submit_password
def submit_password(browser):
    fill_search_field(
        locate_login_input(browser, credentials[2], "password"),
        credentials[3])


def execute_login(browser):
    submit_button = locate_login_input(browser, credentials[4], 'submit')
    submit_button.click()


def verify_login(browser):
    if browser.title == post_login_title:
        print('\nLogin successful, continuing program execution.')
    elif validate_login(browser):
        print('\nLogin successful after validating login, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def open_county_site(browser):
    browser.get(county_site)


def account_login(browser):
    open_site(browser)
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)
    verify_login(browser)
    open_county_site(browser)
