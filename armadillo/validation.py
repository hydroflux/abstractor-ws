from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_value
from settings.general_functions import date_from_string, timeout

from armadillo.armadillo_variables import (bad_login_text,
                                           login_validation_form_name,
                                           login_validation_text_id)


def get_login_validation_text(browser):
    try:
        login_validation_text_present = EC.presence_of_element_locate((By.ID, login_validation_text_id))
        WebDriverWait(browser, timeout).until(login_validation_text_present)
        login_validation_text = browser.find_element_by_id(login_validation_text_id)
        return login_validation_text
    except TimeoutException:
        print('Browser timed out trying to validate login, please review.')


def get_login_validation_form(browser):
    try:
        login_validation_form_present = EC.presence_of_element_located((By.NAME, login_validation_form_name))
        WebDriverWait(browser, timeout).until(login_validation_form_present)
        login_validation_form = browser.find_element_by_name(login_validation_form_name)
        return login_validation_form
    except TimeoutException:
        print('Browser timed out trying to locate login validation form, please review.')


def execute_login_form_validation(browser):
    login_validation_form = get_login_validation_form(browser)
    login_validation_form.submit()
    return True


def validate_login(browser):
    login_validation_text = get_login_validation_text(browser)
    if login_validation_text.startswith(bad_login_text):
        return execute_login_form_validation(browser)


def validate_reception_number(text, document):
    return text.endswith(document_value(document))


def validate_date(text):
    return len(text) == 10 and date_from_string(text) == text


def validate_download_link(document, text):
    return f'{document.reception_number.replace("-", "_")}.pdf' == text