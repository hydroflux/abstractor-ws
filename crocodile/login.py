from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from crocodile.crocodile_variables import website, website_title, credentials, submit_button_id


def open_site(browser):
    browser.get(website)
    assert website_title in browser.title.strip()


def locate_login_field(browser, prompt_id, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.ID, prompt_id))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_id(prompt_id)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} prompt, please review.')


def enter_field_information(field, information):
    field.send_keys(information)


def submit_username(browser):
    username_field = locate_login_field(browser, credentials[0], "username")
    enter_field_information(username_field, credentials[2])


def submit_password(browser):
    password_field = locate_login_field(browser, credentials[1], "password")
    enter_field_information(password_field, credentials[3])


def locate_submit_button(browser):
    try:
        submit_button_present = EC.element_to_be_clickable((By.ID, submit_button_id))
        WebDriverWait(browser, timeout).until(submit_button_present)
        submit_button = browser.find_element_by_id(submit_button_id)
        return submit_button
    except TimeoutException:
        print('Browser timed out trying to locate submit button, please review.')


def execute_login(browser):
    submit_button = locate_submit_button(browser)
    submit_button.click()


def login(browser):
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)