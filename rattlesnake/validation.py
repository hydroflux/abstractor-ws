from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, date_from_string,
                                        timeout)

from rattlesnake.rattlesnake_variables import bad_login_title, post_login_title, document_search_title, home_page_url, home_page_title, post_logout_title


def verify_home_page(browser, document):
    if not assert_window_title(browser, home_page_title):
        print(f'Browser failed to open document search link for '
              f'{extrapolate_document_value(document)}, please review.')
        input()
    else:
        return True


def return_home(browser):
    browser.get(home_page_url)
    return verify_home_page(browser)


# Consolidate validate_login & validate_document_search_page after testing for additional fallbacks
def validate_login(browser, login):
    if check_for_bad_server_response(browser):
        return_home(browser)
        login
        return True


# Consolidate validate_login & check_for_bad_login after testing for additional fallbacks
def check_for_bad_server_response(browser):
    if assert_window_title(browser, post_login_title):
        print('Server returned a bad login response, trying again...')
        return True
    else:
        print('Failed login does not match prepared expectations, please review and try again.')
        input()


def verify_login(browser, login):
    if assert_window_title(browser, post_login_title):
        print('\nLogin successful, continuing program execution.')
    elif validate_login(browser, login):
        print('\nLogin successful after validating login, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def verify_logout(browser):
    if not assert_window_title(browser, post_logout_title):
        print('Browser failed to log out of county system successfully, please review.')
        input()


def verify_document_search_page_loaded(browser, document):
    if not assert_window_title(browser, document_search_title):
        print(f'Browser failed to open document search link for '
              f'{extrapolate_document_value(document)}, please review.')
        input()
    else:
        return True


def validate_document_search_page(browser, search):
    if check_for_bad_server_response(browser):
        return_home(browser)
        search
        return True
