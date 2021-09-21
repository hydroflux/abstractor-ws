from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id as locate_button

from rattlesnake.validation import verify_logout
from rattlesnake.rattlesnake_variables import logout_button_id


def logout(browser):
    click_button(browser, locate_button, logout_button_id, "logout button")
    verify_logout(browser)
