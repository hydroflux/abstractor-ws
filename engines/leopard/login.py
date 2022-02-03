from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout

from settings.county_variables.leopard import (credentials, login_title,
                                               validation_errors_class,
                                               website, website_title)

from engines.leopard.disclaimer import handle_disclaimer

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)

# Script is nearly identical to tiger login--extrapolate into "big cats"


def open_site(browser, abstract):
    browser.get(abstract.county.urls["Login"])
    assert abstract.county.titles["Login"] in browser.title


def locate_login_prompt(browser):
    try:
        login_prompt_open = EC.presence_of_element_located((By.ID, credentials[1]))
        WebDriverWait(browser, timeout).until(login_prompt_open)
        login_prompt = browser.find_element_by_id(credentials[1])
        return login_prompt
    except TimeoutException:
        print("Browser timed out while trying to locate login prompt.")


def enter_credentials(browser):
    login_prompt = locate_login_prompt(browser)
    login_prompt.send_keys(credentials[0] + Keys.TAB + credentials[2] + Keys.RETURN)


def get_validation_errors(browser, abstract):
    try:
        validation_errors_present = EC.presence_of_element_located((By.CLASS_NAME, validation_errors_class))
        WebDriverWait(browser, timeout).until(validation_errors_present)
        validation_errors = browser.find_element_by_class_name(validation_errors_class)
        return validation_errors
    except TimeoutException:
        print("Browser timed out while trying to identify validation errors, please review.")


def verify_login(browser, abstract):
    if browser.title == login_title:
        validation_errors = get_validation_errors(browser)
        print(validation_errors.text)
        browser.quit()
        exit()


def login(browser, abstract):
    open_site(browser, abstract)
    enter_credentials(browser, abstract)
    verify_login(browser, abstract)
    handle_disclaimer(browser)
