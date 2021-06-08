from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from crocodile.crocodile_variables import website, website_title, credentials


def open_site(browser):
    browser.get(website)
    assert website_title in browser.title.strip()


def locate_login_prompt(browser, prompt_id, type):
    try:
        login_prompt_present = EC.presence_of_element_located((By.ID, prompt_id))
        WebDriverWait(browser, timeout).until(login_prompt_present)
        login_prompt = browser.find_element_by_id(prompt_id)
        return login_prompt
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} prompt, please review.')


def enter_credentials(prompt, credential):
    pass


def login(browser):
    pass
