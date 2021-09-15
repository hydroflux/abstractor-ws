from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import get_direct_link, timeout

from armadillo.armadillo_variables import (first_result_class_name, link_tag,
                                           number_results_class,
                                           search_results_id,
                                           single_result_message)
from armadillo.validation import (validate_first_result, verify_results_loaded,
                                  verify_search_results_page_loaded)


def locate_result_count(browser, document):
    try:
        result_count_present = EC.presence_of_element_located((By.CLASS_NAME, number_results_class))
        WebDriverWait(browser, timeout).until(result_count_present)
        result_count = browser.find_element_by_class_name(number_results_class)
        return result_count
    except TimeoutException:
        print(f'Browser timed out trying to locate result count for '
              f'{document.extrapolate_value()}, please review.')
        input()


def count_results(browser, document):
    result_count = locate_result_count(browser, document)
    if result_count.text == single_result_message:
        document.number_results += 1
    else:
        print(f'Browser located multiple search results for '
              f'{document.extrapolate_value()}, new logic path needs to be developed.')
        print("Please press enter after reviewing the search results...")
        input()


def locate_search_results(browser, document):
    try:
        search_results_present = EC.presence_of_element_located((By.ID, search_results_id))
        WebDriverWait(browser, timeout).until(search_results_present)
        search_results = browser.find_element_by_id(search_results_id)
        return search_results
    except TimeoutException:
        print(f'Browser timed out trying to locate search results for '
              f'{document.extrapolate_value()}, please review.')
        input()


def locate_first_result(search_results, document):
    try:
        first_result_present = EC.element_to_be_clickable((By.CLASS_NAME, first_result_class_name))
        WebDriverWait(search_results, timeout).until(first_result_present)
        first_result = search_results.find_element_by_class_name(first_result_class_name)
        return first_result
    except TimeoutException:
        print(f'Browser timed out trying to locate first search result of '
              f'{document.extrapolate_value()}, please review.')
        input()


def get_first_result(browser, document):
    search_results = locate_search_results(browser, document)
    return locate_first_result(search_results, document)


def locate_result_link(document, result):
    try:
        result_link_present = EC.element_to_be_clickable((By.TAG_NAME, link_tag))
        WebDriverWait(result, timeout).until(result_link_present)
        result_link = result.find_element_by_tag_name(link_tag)
        return result_link
    except TimeoutException:
        print(f'Browser timed out trying to locate result link for '
              f'{document.extrapolate_value()}, please review.')
        input()


def access_result_link(document, result):
    result_link_element = locate_result_link(document, result)
    return get_direct_link(result_link_element)


def open_result_link(browser, document, result):
    try:
        document_link = access_result_link(document, result)
        document.description_link = document_link
        browser.get(document.description_link)
        return True
    except TimeoutException:
        print(f'Browser timed out trying to open result link for '
              f'{document.extrapolate_value()}, please review.')
        input()
        return False


def open_first_result(browser, document):
    first_result = get_first_result(browser, document)
    first_result_text = first_result.text.split('\n')
    if validate_first_result(first_result_text, document):
        return open_result_link(browser, document, first_result)


def handle_search_results(browser, document):
    if document.number_results == 1:
        return open_first_result(browser, document)
    else:
        print(f'Document instance indicates that more or less than 1 result were located searching '
              f'{document.extrapolate_value()}, please review (should not have reached this stage)')
        print("Please press enter after reviewing the search parameters...")
        input()
        return False


def open_document(browser, document):
    verify_search_results_page_loaded(browser, document)
    if verify_results_loaded(browser, document):
        count_results(browser, document)
        return handle_search_results(browser, document)
    else:
        return False
