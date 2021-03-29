from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import (credentials, login_button_class, timeout, webpage_title,
                       website)


def open_site(browser):
    browser.get(website)
    assert webpage_title in browser.title
    input("Press enter to login...")


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


def account_login(browser):
    print("Initialized.")
    try:
        open_site(browser)
        open_login_prompt(browser)
        enter_credentials(browser)
        confirm_login(browser)
    except TimeoutException:
        print("Browser timed out while trying to execute login sequence.")
