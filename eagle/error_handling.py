from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import extrapolate_document_value
from settings.general_functions import naptime, timeout

from eagle.eagle_variables import error_message_class, error_message_text


def locate_error_message(browser):
    try:
        error_message_present = EC.presence_of_element_located((By.CLASS_NAME, error_message_class))
        WebDriverWait(browser, timeout).until(error_message_present)
        error_message = browser.find_element_by_class_name(error_message_class)
        return error_message
    except TimeoutException:
        print("Browser timed out while trying to locate error message after PDF failed to load, please review.")


def check_for_error(browser, document):
    error_message = locate_error_message(browser)
    if error_message == error_message_text:
        print(f'An error occurred while opening the document located at '
              f'{extrapolate_document_value(document)}, refreshing the page to try again.')
        browser.refresh()
        naptime()
        return error_message_text
