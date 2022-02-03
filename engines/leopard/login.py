from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout

from engines.leopard.disclaimer import handle_disclaimer
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_id

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)

# Script is nearly identical to tiger login--extrapolate into "big cats"


def open_site(browser, abstract):
    browser.get(abstract.county.urls["Login"])
    assert abstract.county.titles["Login"] in browser.title


def enter_credentials(browser, abstract):
    login_prompt = locate_element_by_id(browser, abstract.county.credentials[1], "login prompt")
    login_prompt.send_keys(abstract.county.credentials[0] + Keys.TAB + abstract.county.credentials[2] + Keys.RETURN)


def verify_login(browser, abstract):
    if browser.title == abstract.county.titles["Login"]:
        validation_errors = locate_element_by_class_name(browser, abstract.county.classes["Validation Error"],
                                                         "validation errors")
        print(validation_errors.text)
        browser.quit()
        exit()


def login(browser, abstract):
    open_site(browser, abstract)
    enter_credentials(browser, abstract)
    verify_login(browser, abstract)
    handle_disclaimer(browser)
