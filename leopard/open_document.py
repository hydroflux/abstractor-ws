from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.settings import timeout
from settings.file_management import extrapolate_document_value

from leopard.leopard_variables import (first_result_tag, result_cell_tag,
                                       result_count_button_id, result_count_class,
                                       results_body_tag, results_id)

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