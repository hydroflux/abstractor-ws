from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from eagle.eagle_variables import (credentials, logged_out_redirect_url, disclaimer_id, inaccessible, 
                                   login_button_class, webpage_title, website)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)


def open_site(browser):
    browser.get(website)
    assert webpage_title in browser.title
    input("Press enter to login...")


def locate_disclaimer(browser):
    try:
        disclaimer_present = EC.presence_of_element_located((By.ID, disclaimer_id))
        WebDriverWait(browser, timeout).until(disclaimer_present)
        disclaimer = browser.find_element_by_id(disclaimer_id)
        return disclaimer
    except NoSuchElementException:
        return False


def handle_disclaimer(browser):
    if not locate_disclaimer(browser):
        return True
    elif locate_disclaimer(browser).get_attribute(inaccessible) is not None:
        return False
    elif locate_disclaimer(browser).get_attribute(inaccessible) is None:
        return True


def check_for_disclaimer(browser):
    while not handle_disclaimer(browser):
        input('Disclaimer has not been handled properly, please press enter after resolving.')


def open_login_prompt(browser):
    try:
        login_button_present = EC.element_to_be_clickable((By.CLASS_NAME, login_button_class))
        WebDriverWait(browser, timeout).until(login_button_present)
        login_button = browser.find_element_by_class_name(login_button_class)
        login_button.click()
    except TimeoutException:
        print("Browser timed out while trying to click login prompt.")


def enter_credentials(browser):
    try:
        login_prompt_open = EC.presence_of_element_located((By.ID, credentials[1]))
        WebDriverWait(browser, timeout).until(login_prompt_open)
        login_prompt = browser.find_element_by_id(credentials[1])
        login_prompt.send_keys(credentials[0] + Keys.TAB + credentials[2] + Keys.RETURN)
    except TimeoutException:
        print("Browser timed out while trying to enter login credentials.")


def read_login_message(browser):
    try:
        login_message_present = EC.presence_of_element_located((By.ID, credentials[4]))
        WebDriverWait(browser, timeout).until(login_message_present)
        return browser.find_element_by_id(credentials[4]).text
    except TimeoutException:
        print("Browser timed out while trying to read login message.")


def confirm_login(browser):
    while read_login_message(browser) != credentials[3]:
        sleep(0.5)


def log_back_in(browser):
    try:
        open_login_prompt(browser)
        enter_credentials(browser)
        confirm_login(browser)
    except TimeoutException:
        print("Browser timed out while trying to log back in after logout.")


def check_login_status(browser):
    if browser.current_url == logged_out_redirect_url:
        print('Web driver timed out, attempting to log back in.')
        log_back_in(browser)


def execute_login_process(browser):
    try:
        open_site(browser)
        check_for_disclaimer(browser)
        open_login_prompt(browser)
        enter_credentials(browser)
        confirm_login(browser)
        return True
    except TimeoutException:
        print("Browser timed out while trying to execute login sequence.")
        return False


def account_login(browser):
    print("\nWebdriver initialized, attempting to login...")
    if not execute_login_process(browser):
        print("Login sequence failed, attempting again before closing out.")
        if not execute_login_process(browser):
            print("Browser failed to properly login, please review & try again later.")
            browser.quit()
            exit()
