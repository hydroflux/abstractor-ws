from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_name)
from selenium_utilities.open import open_url

from engines.tiger.search import open_search


def enter_credentials(browser, abstract):
    enter_input_value(browser,
                      locate_element_by_id,
                      abstract.county.credentials[0],
                      "username input",
                      abstract.county.credentials[1])
    enter_input_value(browser,
                      locate_element_by_id,
                      abstract.county.credentials[2],
                      "password input",
                      abstract.county.credentials[3])
    click_button(browser,
                 locate_element_by_name,
                 abstract.county.buttons["Login"],
                 "login button")


def login(browser, abstract):
    open_url(browser,
             abstract.county.urls["Login"],
             abstract.county.titles["Login"],
             "county site")
    enter_credentials(browser, abstract)
    open_search(browser, abstract)
    click_button(browser,  # Handle Disclaimer
                 locate_element_by_id,
                 abstract.county.buttons["Disclaimer"],
                 "login disclaimer")
