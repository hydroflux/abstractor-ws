from project_management.timers import naptime

from selenium_utilities.open import assert_window_title
from serializers.recorder import date_from_string

from settings.county_variables.rattlesnake import (
    bad_download_title, bad_login_title, document_description_page_title,
    document_image_page_title, home_page_title, home_page_url,
    post_login_title, post_logout_title)


def verify_home_page(browser):
    if not assert_window_title(browser, home_page_title):
        print('Browser failed to return home, please review.')
        input()
    else:
        return True


def return_home(browser):
    browser.get(home_page_url)
    return verify_home_page(browser)


# Consolidate validate_login & check_for_bad_login after testing for additional fallbacks
def check_for_bad_server_response(browser):
    if assert_window_title(browser, bad_login_title):
        print('Server returned a bad login response, trying again...')
        return True
    elif assert_window_title(browser, post_login_title):
        pass
    else:
        print('Failed login does not match prepared expectations, please review and try again.')
        input()


# Consolidate validate_login & validate_document_search_page after testing for additional fallbacks
def validate_login(browser, login):
    if check_for_bad_server_response(browser):
        return_home(browser)
        naptime()
        login(browser)
        return True


def verify_login(browser, login):
    if assert_window_title(browser, post_login_title):
        print('\nLogin successful, continuing program execution.')
    elif validate_login(browser, login) and assert_window_title(browser, post_login_title):
        print('\nLogin successful after validating login, continuing program execution.')
    else:
        print('\nBrowser failed to successfully login, exiting program.')
        browser.quit()
        exit()


def verify_logout(browser):
    if not assert_window_title(browser, post_logout_title):
        print('Browser failed to log out of county system successfully, please review.')
        input()


# def validate_document_search_page(browser, document, open_search):
#     if check_for_bad_server_response(browser):
#         return_home(browser)
#         open_search(browser)
#         return True


# def verify_document_search_page_loaded(browser, document, search):
#     if assert_window_title(browser, document_search_title):
#         return True
#     elif (validate_document_search_page(browser, document, search) and
#           assert_window_title(browser, document_search_title)):
#         print('Browser failed to open search page on initial attempt, continuing after validation.')
#     else:
#         print(f'Browser failed to open document search link for '
#               f'{document.extrapolate_value()}, please review.')
#         input()


def validate_result_reception_number(result, document):
    return document.value in result.text.split()


def validate_result_volume_and_page_numbers(result, document):
    return all(value in result.text.split() for value in document.document_value())


def verify_document_description_page_loaded(browser, document):
    if assert_window_title(browser, document_description_page_title):
        return True
    else:
        print(f'Browser failed to open document description page for '
              f'{document.extrapolate_value()}, please review')
        input()


def validate_reception_number(document, value):
    return document.value == value


def validate_volume_and_page_numbers(document, volume, page):
    return document.value['Volume'] == int(volume) and document.value['Page'] == int(page)


# Copied directory from armadillo validation (should probably extrapolate to general_functions)
def validate_date(text):
    return len(text) == 10 and date_from_string(text) == text


def validate_document_image_page(browser, document):
    if check_for_bad_server_response(browser):
        return_home(browser)
        browser.get(document.description_link)
        return True


def verify_document_image_page_loaded(browser, document):
    if assert_window_title(browser, document_image_page_title):
        return True
    elif validate_document_image_page(browser, document) and assert_window_title(browser, document_image_page_title):
        print('Browser failed to open document image page on initial attempt, continuing after validation.')
    else:
        print(f'Browser failed to open document image page for '
              f'{document.extrapolate_value()}, please review.')
        input()


def verify_valid_download(browser):
    if assert_window_title(browser, bad_download_title):
        return False
    else:
        return True


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
