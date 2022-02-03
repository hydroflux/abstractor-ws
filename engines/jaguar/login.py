from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_name
from selenium_utilities.open import open_url

from settings.county_variables.jaguar import home_page_title, home_page_url, login_button_name


def login(browser, abstract):
    open_url(browser, home_page_url, home_page_title, "county site")
    click_button(browser, locate_element_by_name, login_button_name, "login button")
