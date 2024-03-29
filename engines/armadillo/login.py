from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)

from project_management.timers import micro_nap

from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)
from selenium_utilities.open import open_url

from engines.armadillo.disclaimer import check_for_disclaimer


def open_site(browser, abstract):
    open_url(browser, abstract.county.urls["Home Page"],
             abstract.county.titles["Home Page"], "county site")
    input("Press enter to login...")


def enter_credentials(browser, abstract):
    enter_input_value(browser, locate_element_by_id, abstract.county.ids["Username"],
                      "username input", abstract.county.credentials[0])
    enter_input_value(browser, locate_element_by_id, abstract.county.ids["Password"],
                      "password input", abstract.county.credentials[1])
    click_button(browser, locate_element_by_id, abstract.county.buttons["Login"], "login button")


def read_login_message(browser, abstract):
    try:
        login_message = locate_element_by_id(browser, abstract.county.ids["Welcome"],
                                             "login message", True)
        return login_message.text
    except StaleElementReferenceException:
        print('Encountered StaleElementReferenceException '
              'attempting to read login message, trying again.')


def confirm_login(browser, abstract):
    while read_login_message(browser, abstract) != abstract.county.credentials[2]:
        micro_nap()


def log_back_in(browser, abstract):
    try:
        click_button(browser, locate_element_by_class_name, abstract.county.classes["Login Prompt"],
                     abstract.county.buttons["Login"], "login button prompt")
        enter_credentials(browser, abstract)
        confirm_login(browser, abstract)
    except TimeoutException:
        print("Browser timed out while trying to log back in after logout.")


# def check_login_status(browser, abstract):
#     check_for_disclaimer(browser, abstract)
#     while browser.current_url == abstract.county.urls["Log Out Redirect"]:
#         print('Browser redirected to login screen, checking login status & returning to search.')
#         if read_login_message(browser, abstract) != abstract.county.credentials[2]:
#             print('Browser logged out, attempting to log back in.')
#             log_back_in(browser, abstract)
#         browser.get(abstract.county.urls["Fallback Search"])


def execute_login_process(browser, abstract):
    open_site(browser, abstract)
    check_for_disclaimer(browser, abstract)
    click_button(browser, locate_element_by_class_name, abstract.county.classes["Login Prompt"],
                 abstract.county.buttons["Login"], "login button prompt")
    enter_credentials(browser, abstract)
    confirm_login(browser, abstract)
    return True


def login(browser, abstract):
    print("\nWebdriver initialized, attempting to login...")
    if not execute_login_process(browser, abstract):
        print("Login sequence failed, attempting again before closing out.")
        if not execute_login_process(browser, abstract):
            print("Browser failed to properly login, please review & try again later.")
            browser.quit()
            exit()