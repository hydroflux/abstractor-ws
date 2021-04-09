from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)

from settings.settings import empty_value, not_applicable, timeout
from settings.file_management import extrapolate_document_value
from settings.general_functions import get_element_text

from leopard.leopard_variables import (book_page_abbreviation,
                                       document_image_id,
                                       document_information_id, document_table_tag,
                                       empty_values, row_data_tag, row_titles,
                                       table_row_tag)


def document_image_loaded(browser, document):
    try:
        document_image_present = EC.presence_of_element_located((By.ID, document_image_id))
        WebDriverWait(browser, timeout).until(document_image_present)
    except TimeoutException:
        print(f'Browser timed out while waiting for '
              f'{extrapolate_document_value(document)} document image to load.')


def get_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_id(document_information_id)
        return document_information
    except TimeoutException:
        print(f'Browser timed out while waiting for '
              f'{extrapolate_document_value(document)} document information to load.')


def document_loaded(browser, document):
    document_image_loaded(browser, document)
    return get_document_information(browser, document)


def get_document_table_data(browser, document_information, document):
    try:
        document_table_data_present = EC.presence_of_element_located((By.TAG_NAME, document_table_tag))
        WebDriverWait(browser, timeout).until(document_table_data_present)
        document_table_data = document_information.find_element_by_tag_name(document_table_tag)
    except TimeoutException:
        print(f'Browser timed out while getting table data for '
              f'{extrapolate_document_value(document)}.')


def get_table_rows(browser, document_table, document):
    try:
        table_rows_present = EC.presence_of_element_located((By.TAG_NAME, table_row_tag))
        WebDriverWait(browser, timeout).until(table_rows_present)
        table_rows = document_table.find_elements_by_tag_name(table_row_tag)
        return table_rows
    except TimeoutException:
        print(f'Browser timed out while getting table rows for '
              f'{extrapolate_document_value(document)}.')


def get_document_content(browser, document):
    document_information = document_loaded(browser, document)
    document_table = get_document_table_data(browser, document_information, document)
    return get_table_rows(browser, document_table, document)
