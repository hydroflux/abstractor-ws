from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from leopard.leopard_variables import (credentials, disclaimer_active_class,
                                       disclaimer_button_id, disclaimer_id,
                                       website, website_title)
from leopard.search import open_search

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


def locate_disclaimer(browser):
    try:
        disclaimer_present = EC.presence_of_element_located((By.ID, disclaimer_id))
        WebDriverWait(browser, timeout).until(disclaimer_present)
        disclaimer = browser.find_element_by_id(disclaimer_id)
        return disclaimer
    except TimeoutException:
        print("Browser timed out while trying to locate disclaimer while logging in, please review.")


def locate_disclaimer_button(browser):
    try:
        disclaimer_button_present = EC.element_to_be_clickable((By.ID, disclaimer_button_id))
        WebDriverWait(browser, timeout).until(disclaimer_button_present)
        disclaimer_button = browser.find_element_by_id(disclaimer_button_id)
        return disclaimer_button
    except TimeoutException:
        print("Browser timed out while trying to locate disclaimer button while logging in, please review.")


def handle_disclaimer(browser):
    disclaimer = locate_disclaimer(browser)
    if disclaimer.get_attribute('class') == disclaimer_active_class:
        disclaimer_button = locate_disclaimer_button(browser)
        disclaimer_button.click()


def account_login(browser):
    open_site(browser)
    enter_credentials(browser)
    open_search(browser)
    handle_disclaimer(browser)
