from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout

from engines.leopard.disclaimer import handle_disclaimer
from selenium_utilities.locators import locate_element_by_id

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)

# Script is nearly identical to tiger login--extrapolate into "big cats"


def open_site(browser, abstract):
    browser.get(abstract.county.urls["Login"])
    assert abstract.county.titles["Login"] in browser.title


def enter_credentials(browser, abstract):
    login_prompt = locate_element_by_id(browser, abstract.county.credentials[1], "login prompt")
    login_prompt.send_keys(abstract.county.credentials[0] + Keys.TAB + abstract.county.credentials[2] + Keys.RETURN)


def get_validation_errors(browser, abstract):
    try:
        validation_errors_present = EC.presence_of_element_located((By.CLASS_NAME, abstract.county.classes["Validation Error"]))
        WebDriverWait(browser, timeout).until(validation_errors_present)
        validation_errors = browser.find_element_by_class_name(abstract.county.classes["Validation Error"])
        return validation_errors
    except TimeoutException:
        print("Browser timed out while trying to identify validation errors, please review.")


def verify_login(browser, abstract):
    if browser.title == abstract.county.titles["Login"]:
        validation_errors = get_validation_errors(browser, abstract)
        print(validation_errors.text)
        browser.quit()
        exit()


def login(browser, abstract):
    open_site(browser, abstract)
    enter_credentials(browser, abstract)
    verify_login(browser, abstract)
    handle_disclaimer(browser)
