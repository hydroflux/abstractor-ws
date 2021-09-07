from armadillo.validation import validate_search_result
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_value, extrapolate_document_value
from settings.general_functions import assert_window_title, get_direct_link, set_description_link, timeout

from armadillo.armadillo_variables import (document_search_results_title,
                                           number_results_class,
                                           search_results_id,
                                           single_result_message, first_result_tag_name)


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
        document.number_results += 1
    else:
        print(f'Browser located multiple search results for '
              f'{extrapolate_document_value(document)}, new logic path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()


def locate_search_results(browser, document):
    try:
        search_results_present = EC.presence_of_element_located((By.ID, search_results_id))
        WebDriverWait(browser, timeout).until(search_results_present)
        search_results = browser.find_element_by_id(search_results_id)
        return search_results
    except TimeoutException:
        print(f'Browser timed out trying to locate search results for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_first_result(search_results, document):
    try:
        first_result_present = EC.element_to_be_clickable((By.TAG_NAME, first_result_tag_name))
        WebDriverWait(search_results, timeout).until(first_result_present)
        first_result = search_results.find_element_by_tag_name(first_result_tag_name)
        return first_result
    except TimeoutException:
        print(f'Browser timed out trying to locate first search result of '
              f'{extrapolate_document_value(document)}, please review.')


def get_first_result(browser, document):
    search_results = locate_search_results(browser, document)
    return locate_first_result(search_results, document)


def open_first_result(browser, document):
    first_result = get_first_result(browser, document)
    if validate_search_result(first_result, document):
        document_link = get_direct_link(first_result)
        set_description_link(document, document_link)
        browser.get(document.description_link)


def handle_search_results(browser, document):
    if document.number_results == 1:
        open_first_result(browser, document)
    else:
        print(f'Document instance indicates that more or less than 1 result were located searching '
              f'{extrapolate_document_value(document)}, please review (should not have reached this stage)')
        print("Please press enter after reviewing the search parameters...")
        input()


def open_document(browser, document):
    verify_successful_search(browser, document)
    count_results(browser, document)
    handle_search_results(browser, document)
