from selenium_utilities.inputs import click_button as submit_login
from selenium_utilities.inputs import enter_input_value as enter_credentials
from selenium_utilities.locators import locate_element_by_name as locate_input
from settings.general_functions import assert_window_title

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
        print('Browser failed to successfully login page, please review.')
        browser.close()
        quit()


def account_login(browser):
    open_site(browser)
    open_login_prompt(browser)
    enter_credentials(browser, locate_input, credentials[0], "username input", credentials[1])
    enter_credentials(browser, locate_input, credentials[2], "password input", credentials[3])
    submit_login(browser, locate_input, credentials[4], 'submit')
    verify_login(browser, account_login)
