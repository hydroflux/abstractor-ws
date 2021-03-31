from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import (first_result_tag, result_cell_tag,
                        result_count_button_id, result_count_id,
                        results_body_tag, results_id, timeout)


def open_result_count(browser, document_number):
    try:
        result_count_button_present = EC.element_to_be_clickable((By.ID, result_count_button_id))
        WebDriverWait(browser, timeout).until(result_count_button_present)
        result_count_button = browser.find_element_by_id(result_count_button_id)
        result_count_button.click()
    except TimeoutException:
        print(f'Browser timed out trying to open the number of results for document number {document_number}.')


def count_results(browser, document_number):
    try:
        result_count_present = EC.presence_of_element_located((By.ID, result_count_id))
        WebDriverWait(browser, timeout).until(result_count_present)
        result_count = browser.find_element_by_id(result_count_id)
        return result_count.text.split(' ')[-1]
    except TimeoutException:
        print(f'Browser timed out trying to read the number of results for document number {document_number}.')


def identify_first_result(browser, document_number):
    try:
        results_present = EC.presence_of_element_located((By.ID, results_id))
        WebDriverWait(browser, timeout).until(results_present)
        results = browser.find_element_by_id(results_id)
        results_body = results.find_element_by_tag_name(results_body_tag)
        return results_body.find_element_by_tag_name(first_result_tag)
    except TimeoutException:
        print(f'Browser timed out trying to identify first result after searching document number {document_number}.')


def get_element_text(element):
    return element.text


def check_result(browser, document_number):
    first_result = identify_first_result(browser, document_number)
    first_result_cells = first_result.find_elements_by_tag_name(result_cell_tag)
    if document_number in map(get_element_text, first_result_cells):
        return True


def open_document_result(browser, document_number):
    if check_result(browser, document_number):
        identify_first_result(browser, document_number).click()
