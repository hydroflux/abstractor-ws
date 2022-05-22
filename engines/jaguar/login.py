from selenium.common.exceptions import StaleElementReferenceException

from project_management.timers import micro_nap

from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)
from selenium_utilities.open import open_url


def enter_credentials(browser, abstract):
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[0],
                      "username input", abstract.county.credentials[1])
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[2],
                      "password input", abstract.county.credentials[3])
    click_button(browser, locate_element_by_id, abstract.county.buttons["Login"], "login button")


def read_login_message(browser, abstract):
    try:
        login_message = locate_element_by_id(browser, abstract.county.credentials[4],
                                             "login message", True)
        return login_message.text
    except StaleElementReferenceException:
        print('Encountered StaleElementReferenceException '
              'attempting to read login message, trying again.')


def confirm_login(browser, abstract):
    while read_login_message(browser, abstract) != abstract.county.credentials[5]:
        micro_nap()


def execute_login_process(browser, abstract):
    open_url(browser, abstract.county.urls["Home Page"],
             abstract.county.titles["Home Page"], "county site")
    click_button(browser, locate_element_by_class_name, abstract.county.classes["Login Prompt"],
                 abstract.county.buttons["Login"], "login button prompt")
    enter_credentials(browser, abstract)
    confirm_login(browser, abstract)
    return True


def login(browser, abstract):
    if not execute_login_process(browser, abstract):
        print("Login sequence failed, attempting again before closing out.")
        if not execute_login_process(browser, abstract):
            print("Browser failed to properly login, please review & try again later.")
            browser.quit()
            exit()
