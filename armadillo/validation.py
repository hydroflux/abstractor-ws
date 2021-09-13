from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, date_from_string,
                                        timeout)

from armadillo.armadillo_variables import (bad_login_text,
                                           document_information_title,
                                           document_search_results_title,
                                           document_search_title,
                                           login_validation_form_name,
                                           login_validation_text_id,
                                           post_login_title)


def get_login_validation_text(browser):
    try:
        login_validation_text_present = EC.presence_of_element_located((By.ID, login_validation_text_id))
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
    login_validation_information = get_login_validation_text(browser)
    if login_validation_information.text.startswith(bad_login_text):
        return execute_login_form_validation(browser)


def verify_login(browser):
    if assert_window_title(browser, post_login_title):
        print('\nLogin successful, continuing program execution.')
    elif validate_login(browser):
        print('\nLogin successful after validating login, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def verify_document_search_page_loaded(browser, document):
    if not assert_window_title(browser, document_search_title):
        print(f'Browser failed to open document search link for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def verify_search_results_loaded(browser, document):
    if not assert_window_title(browser, document_search_results_title):
        print(f'Browser failed to successfully execute search for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def verify_results_page_loaded(browser, document):
    if not assert_window_title(browser, document_information_title):
        print(f'Browser failed to successfully open results page for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def validate_reception_number(string, document):
    return string.endswith(document.value)


# Used again for rattlesnake
def validate_date(text):
    return len(text) == 10 and date_from_string(text) == text


def validate_download_link(document, string):
    return f'{document.value.replace("-", "_")}.pdf' == string


'''
Validate vs. Verify

Validation is the process of checking whether the specification
captures the customer's requirements, while verification is the
process of checking that the software meets specifications.

~~ VERIFICATION ~~
A test of a system to prove that it meets all its specified
requirements at a particular stage of its development.

~~ VALIDATION ~~
An activity that ensures that an end product stakeholder’s
true needs and expectations are met.
'''
