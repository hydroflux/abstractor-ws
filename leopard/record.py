from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)

from settings.settings import empty_value, not_applicable, timeout
from settings.file_management import extrapolate_document_value

from leopard.leopard_variables import (book_page_abbreviation,
                                       document_image_id,
                                       document_information_id, document_tag,
                                       empty_values, row_data_tag, row_titles,
                                       table_row_tag)


def document_image_loaded(browser, document):
    try:
        document_image_present = EC.presence_of_element_located((By.ID, document_image_id))
        WebDriverWait(browser, timeout).until(document_image_present)
    except TimeoutException:
        print(f'Browser timed out while waiting for '
              f'{extrapolate_document_value(document)} document image to load.')


def document_information_loaded(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        return browser.find_element_by_id(document_information_id)
    except TimeoutException:
        print(f'Browser timed out while waiting for '
              f'{extrapolate_document_value(document)} document information to load.')


def document_loaded(browser, document):
    document_image_loaded(browser, document)
    return document_information_loaded(browser, document)