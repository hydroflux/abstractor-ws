from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_value, extrapolate_document_value
from settings.settings import timeout

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open_document", __name__)

from leopard.leopard_variables import (first_result_tag, result_cell_tag,
                                       result_count_button_id,
                                       result_count_class, results_body_tag,
                                       results_id)

# Script is SIMILAR, but not nearly identical, to tiger open_document

def count_results(browser, document):
    try:
        result_count_present = EC.presence_of_element_located((By.CLASS_NAME, result_count_class))
        WebDriverWait(browser, timeout).until(result_count_present)
        result_count = browser.find_element_by_class_name(result_count_class)
        return result_count.text.split(' ')[-1]
    except TimeoutException:
        print(f'Browser timed out trying to read the number of results for '
              f'{extrapolate_document_value(document)}.')


def identify_first_result(browser, document):
    try:
        results_present = EC.presence_of_element_located((By.ID, results_id))
        WebDriverWait(browser, timeout).until(results_present)
        results = browser.find_element_by_id(results_id)
        browser.execute_script("arguments[0].scrollIntoView();", results)
        results_body = results.find_element_by_tag_name(results_body_tag)
        return results_body.find_element_by_tag_name(first_result_tag)
    except TimeoutException:
        print(f'Browser timed out trying to identify first result after searching '
              f'{extrapolate_document_value(document)}.')


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
