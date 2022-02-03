from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id as locate_button

from engines.rattlesnake.validation import verify_logout
from settings.county_variables.rattlesnake import logout_button_id


def logout(browser, abstract):
    click_button(browser, locate_button, logout_button_id, "logout button")
    verify_logout(browser)
