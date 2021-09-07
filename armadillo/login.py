from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import (assert_window_title, fill_search_field,
                                        timeout)

from armadillo.armadillo_variables import (credentials, post_login_title,
                                            website, website_title)


# Identical to buffalo open_site
def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()


# Identical to buffalo open_site
def locate_login_field(browser, prompt_name, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.NAME, prompt_name))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_name(prompt_name)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} prompt, please review.')


def submit_username(browser):
    pass


def submit_password(password):
    pass


def execute_login(browser):
    pass


def verify_login(browser):
    pass


def account_login(browser):
    open_site(browser)
    submit_username(browser)
    submit_password(browser)
    execute_login(browser)
    verify_login(browser)
