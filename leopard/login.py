from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from leopard.disclaimer import handle_disclaimer
from leopard.leopard_variables import (credentials, login_title,
                                       validation_errors_class, website,
                                       website_title)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)

# Script is nearly identical to tiger login--extrapolate into "big cats"


def open_site(browser):
    browser.get(website)
    assert website_title in browser.title


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


def get_validation_errors(browser):
    try:
        validation_errors_present = EC.presence_of_element_located((By.CLASS_NAME, validation_errors_class))
        WebDriverWait(browser, timeout).until(validation_errors_present)
        validation_errors = browser.find_element_by_class_name(validation_errors_class)
        return validation_errors
    except TimeoutException:
        print("Browser timed out while trying to identify validation errors, please review.")


def verify_login(browser):
    if browser.title == login_title:
        validation_errors = get_validation_errors(browser)
        print(validation_errors.text)
        browser.quit()
        exit()


def account_login(browser):
    open_site(browser)
    enter_credentials(browser)
    verify_login(browser)
    handle_disclaimer(browser)
