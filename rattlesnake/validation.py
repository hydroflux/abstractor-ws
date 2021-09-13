from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, date_from_string,
                                        timeout)

from rattlesnake.rattlesnake_variables import bad_login_title


def validate_login(browser, login):
    if check_for_bad_login(browser):
        login
        return True


# Consolidate validate_login & check_for_bad_login after testing for additional fallbacks
def check_for_bad_login(browser):
    if browser.title == bad_login_title:
        print('Server returned a bad login response, trying again...')
        return True
    else:
        print('Failed login does not match prepared expectations, please review and try again.')
        input()


def verify_login(browser, login):
    if browser.title == post_login_title:
        print('\nLogin successful, continuing program execution.')
    elif validate_login(browser, login):
        print('\nLogin successful after validating login, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()
