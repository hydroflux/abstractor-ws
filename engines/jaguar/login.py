from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_name
from selenium_utilities.open import open_url


def login(browser, abstract):
    open_url(browser, abstract.county.urls["Home"], abstract.county.titles["Home"], "county site")
    click_button(browser, locate_element_by_name, abstract.county.buttons["Login"], "login button")
