from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import javascript_script_execution, timeout

from armadillo.armadillo_variables import login_validation_text_id, bad_login_text


def get_login_validation_text(browser):
    try:
        login_validation_text_present = EC.presence_of_element_locate((By.ID, login_validation_text_id))
        WebDriverWait(browser, timeout).until(login_validation_text_present)
        login_validation_text = browser.find_element_by_id(login_validation_text_id)
        return login_validation_text
    except TimeoutException:
        print('Browser timed out trying to validate login, please review.')


def execute_form_validation(browser):
    pass


def validate_login(browser):
    login_validation_text = get_login_validation_text(browser)
    if login_validation_text.startswith(bad_login_text):
        execute_form_validation(browser)
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()

