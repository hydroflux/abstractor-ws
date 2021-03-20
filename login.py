
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import website, webpage_title, credentials, login_button_class, timeout

def open_site(browser):
    browser.get(website)
    assert webpage_title in browser.title
    input("Press enter to login...")

def accept_conditions(browser):
    try:
        accept_conditions_present = EC.element_to_be_clickable()

def open_login_prompt(browser):
    try:
        login_button_present = EC.element_to_be_clickable((By.CLASS_NAME, login_button_class))
        WebDriverWait(browser, timeout).until(login_button_present)
        login_button = browser.find_element_by_class(login_button_class)
        login_button.click()
    except TimeoutException:
        print("Browser timed out while trying to click login prompt.")

def enter_credentials(browser):
    try:
        login_prompt_open = EC.presence_of_element_located((By.ID, user_id))
        WebDriverWait(browser, timeout).until(login_prompt_open)
        login_prompt = browser.find_element_by_id(user_id)
        login_prompt.send_keys(credentials[0] + Keys.TAB + credentials[1] + Keys.RETURN)
    except TimeoutException:
        print("Browser timed out while trying to enter login credentials.")

def account_login(browser):
    open_site(browser)
    open_login_prompt(browser)
    enter_credentials(browser)
