from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.settings import timeout

from tiger.search import open_search
from tiger.tiger_variables import (credentials, handle_disclaimer_id, website,
                                   website_title)


def open_site(browser):
    browser.get(website)
    assert website_title in browser.title


def enter_credentials(browser):
    try:
        login_prompt_open = EC.presence_of_element_located((By.ID, credentials[1]))
        WebDriverWait(browser, timeout).until(login_prompt_open)
        login_prompt = browser.find_element_by_id(credentials[1])
        login_prompt.send_keys(credentials[0] + Keys.TAB + credentials[2] + Keys.RETURN)
    except TimeoutException:
        print("Browser timed out while trying to enter login credentials.")


def handle_disclaimer(browser):
    try:
        disclaimer_present = EC.element_to_be_clickable((By.ID, handle_disclaimer_id))
        WebDriverWait(browser, timeout).until(disclaimer_present)
        disclaimer = browser.find_element_by_id(handle_disclaimer_id)
        disclaimer.click()
    except TimeoutException:
        print("Browser timed out while trying to handle the website disclaimer.")


def login(browser):
    open_site(browser)
    enter_credentials(browser)
    open_search(browser)
    handle_disclaimer(browser)
