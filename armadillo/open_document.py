from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_value, extrapolate_document_value
from settings.general_functions import assert_window_title, timeout

from armadillo.armadillo_variables import number_results_class, search_results_id, document_search_results_title, single_result_message


def verify_successful_search(browser, document):
    if not assert_window_title(browser, document_search_results_title):
        print(f'Browser failed to successfully execute search for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def locate_result_count(browser, document):
    try:
        result_count_present = EC.presence_of_element_located((By.CLASS_NAME, number_results_class))
        WebDriverWait(browser, timeout).until(result_count_present)
        result_count = browser.find_element_by_class_name(number_results_class)
        return result_count
    except TimeoutException:
        print(f'Browser timed out trying to locate result count for '
              f'{extrapolate_document_value(document)}, please review.')


def count_results(browser, document):
    result_count = locate_result_count(browser, document)
    if result_count == single_result_message:
        return 1
    else:
        print(f'Browser located multiple search results for '
              f'{extrapolate_document_value(document)}, new logic path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def open_document(browser, document):
    verify_successful_search(browser, document)
    if count_results == 1:
        pass
