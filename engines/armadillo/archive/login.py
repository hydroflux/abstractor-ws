from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_name as locate_input
from selenium_utilities.open import open_url

from settings.county_variables.armadillo import credentials, login_title, login_url

from engines.armadillo.validation import verify_login


def enter_credentials(browser):
    enter_input_value(browser, locate_input, credentials[0],  # Submit Username
                      "username input", credentials[1])
    enter_input_value(browser, locate_input, credentials[2],  # Submit Password
                      "password input", credentials[3])
    click_button(browser, locate_input, credentials[4], 'submit')  # Click Login Button


def account_login(browser):
    open_url(browser, login_url, login_title, "county site")  # Open County Site
    enter_credentials(browser)  # Enter Login Information
    verify_login(browser)  # Verify Login
