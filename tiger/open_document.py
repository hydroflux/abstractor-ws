from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_utilities.element_interaction import center_element

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id, locate_element_by_tag_name

from settings.county_variables.tiger import (first_result_tag, result_cell_tag,
                                             result_count_button_id,
                                             result_count_id, results_body_tag,
                                             results_id)
from settings.file_management import document_value, extrapolate_document_value
from settings.general_functions import scroll_into_view, timeout


def count_results(browser, document):
    click_button(browser, locate_element_by_id, result_count_button_id,
                 "result count button", document)  # Open Result Count
    result_count = locate_element_by_id(browser, result_count_id,
                                        "result count", document=document)  # Get Result Count
    return result_count.text.split(' ')[-1]


def get_results_table_body(browser, document):
    results = locate_element_by_id(browser, results_id,
                                   "results section", document=document)
    center_element(browser, results)
    results_table = locate_element_by_tag_name(browser, results_body_tag,
                                               "results table", document=document)
    return results_table


def get_all_results(browser, results_table_body, document):
    try:
        first_row_present = EC.presence_of_element_located((By.TAG_NAME, first_result_tag))
        WebDriverWait(browser, timeout).until(first_row_present)
        all_results = results_table_body.find_elements_by_tag_name(first_result_tag)
        return all_results
    except TimeoutException:
        print(f'Browser timed out while trying to get results for '
              f'{extrapolate_document_value(document)}, please review.')


def get_first_row(browser, results_table_body, document):
    all_results = get_all_results(browser, results_table_body, document)
    return all_results[0]


def identify_first_result(browser, document):
    results_table_body = get_results_table_body(browser, document)
    return get_first_row(browser, results_table_body, document)


def get_element_text(element):
    return element.text


def check_result(browser, document):
    first_result = identify_first_result(browser, document)
    first_result_cells = first_result.find_elements_by_tag_name(result_cell_tag)
    if document_value(document) in map(get_element_text, first_result_cells):
        return True


def open_document(browser, document):
    count_results(browser, document)
    if check_result(browser, document):
        identify_first_result(browser, document).click()
        return True
