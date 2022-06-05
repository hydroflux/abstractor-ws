from project_management.timers import micro_nap

from selenium_utilities.element_interaction import get_element_class
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_elements_by_class_name)
from selenium_utilities.open import open_url


def enter_credentials(browser, abstract):
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[0],
                      "username input", abstract.county.credentials[1])
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[2],
                      "password input", abstract.county.credentials[3])
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Login"], "login button")


def check_for_redirect(browser, abstract):
    micro_nap()
    redirect_modal = locate_element_by_id(browser, abstract.county.ids["Redirect Modal"], "redirect modal")
    if redirect_modal is None:
        return
    elif get_element_class(redirect_modal) == abstract.county.classes["Redirect Active"]:
        buttons = locate_elements_by_class_name(browser, abstract.county.buttons["Login"],
                                                "login buttons", True)
        buttons[2].click()


def login(browser, abstract):
    open_url(browser, abstract.county.urls["Login Page"],
             abstract.county.titles["Login Page"], "county site")
    enter_credentials(browser, abstract)
    check_for_redirect(browser, abstract)
    open_url(browser, abstract.county.urls["Home Page"],
             abstract.county.titles["Home Page"], "county site")
