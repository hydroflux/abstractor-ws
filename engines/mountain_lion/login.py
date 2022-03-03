from engines.mountain_lion.iframe_handling import switch_to_main_frame
from selenium_utilities.inputs import enter_input_value
from selenium_utilities.locators import locate_element_by_name
from selenium_utilities.open import assert_window_title, open_url

from settings.general_functions import javascript_script_execution


def enter_credentials(browser, abstract):
    enter_input_value(browser, locate_element_by_name, abstract.county.credentials[0],
                      "username input", abstract.county.credentials[1])
    enter_input_value(browser, locate_element_by_name, abstract.county.credentials[2],
                      "password input", abstract.county.credentials[3])


# Move to disclaimer script
def handle_disclaimer(browser, abstract):
    switch_to_main_frame(browser, abstract)
    javascript_script_execution(browser, abstract.county.scripts['Disclaimer'])


def execute_login(browser, abstract):
    javascript_script_execution(browser, abstract.county.scripts['Login'])
    handle_disclaimer(browser, abstract)
    assert_window_title(browser, abstract.county.titles['Post Login'])


def login(browser, abstract):
    print("\nWebdriver initialized, attempting to login...")
    open_url(browser, abstract.county.urls["Login"], abstract.county.titles["Login"], "login")
    enter_credentials(browser, abstract)
    execute_login(browser, abstract)
