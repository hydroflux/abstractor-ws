from buffalo.frame_handling import switch_to_main_frame
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import assert_window_title, fill_search_field, javascript_script_execution, timeout

from buffalo.buffalo_variables import (credentials, website, website_title, login_script, disclaimer_button_id, disclaimer_script, post_login_title, post_login_text, welcome_message_id)


def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


def locate_login_field(browser, prompt_name, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.NAME, prompt_name))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_name(prompt_name)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} prompt, please review.')


def submit_username(browser):
    fill_search_field(locate_login_field(browser, credentials[0], "username"), credentials[1])


def submit_password(browser):
    fill_search_field(locate_login_field(browser, credentials[2], "password"), credentials[3])


def execute_login(browser):
    javascript_script_execution(browser, login_script)
    assert_window_title(browser, post_login_title)


def handle_disclaimer(browser):
    switch_to_main_frame(browser)
    javascript_script_execution(browser, disclaimer_script)


def locate_post_login_message(browser):
    try:
        welcome_message_present = EC.presence_of_element_located((By.ID, welcome_message_id))
        WebDriverWait(browser, timeout).until(welcome_message_present)
        welcome_message = browser.find_element_by_id(welcome_message_id)
        return welcome_message
    except TimeoutException:
        print("Browser timed out trying to locate post login welcome message, please review.")


def verify_login(browser):
    switch_to_main_frame(browser)
    welcome_message = locate_post_login_message(browser)
    if welcome_message.text == post_login_text:
        print('\nLogin successful, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def account_login(browser):
    open_site(browser)
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)
    handle_disclaimer(browser)
    verify_login(browser)
