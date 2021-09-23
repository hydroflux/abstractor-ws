from selenium_utilities.open import assert_window_title
from selenium_utilities.locators import locate_element_by_name as locate_input
from selenium_utilities.inputs import click_button, enter_input_value

from armadillo.armadillo_variables import credentials, website, website_title
from armadillo.validation import verify_login


# Identical to buffalo open_site
def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


def enter_credentials(browser):
    enter_input_value(browser, locate_input, credentials[0],  # Submit Username
                      "username input", credentials[1])
    enter_input_value(browser, locate_input, credentials[2],  # Submit Password
                      "password input", credentials[3])
    click_button(browser, locate_input, credentials[4], 'submit')  # Click Login Button    


def account_login(browser):
    open_site(browser)
    enter_credentials(browser)
    verify_login(browser)
