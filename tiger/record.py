from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import timeout


def record_bad_search(dataframe, document_number):
    bad_search_message = f'No document found at reception number {document_number}'
    dataframe["Grantor"].append(search_errors[0])
    dataframe["Grantee"].append(search_errors[0])
    dataframe["Book"].append(search_errors[2])
    dataframe["Page"].append(search_errors[2])
    dataframe["Reception Number"].append(document_number)
    dataframe["Document Type"].append(search_errors[0])
    dataframe["Recording Date"].append(search_errors[1])
    dataframe["Legal"].append(search_errors[2])
    dataframe["Related Documents"].append(search_errors[2])
    dataframe["Comments"].append(bad_search_message)

def document_image_loaded(browser, document_number):
    try:
        document_image_present = EC.presence_of_element_located((By.ID, document_image_id))
        WebDriverWait(browser, timeout).until(document_image_present)
    except TimeoutException:
        print(f'Browser timed out while waiting for the document {document_number} image to load.')


def document_information_loaded(browser, document_number):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        return browser.find_element_by_id(document_information_id)
    except TimeoutException:
        print(f'Browser timed out while waiting for the document {document_number} information to load.')


def document_loaded(browser, document_number):
    document_image_loaded(browser, document_number)
    return document_information_loaded(browser, document_number)


def document_table_data(browser, document_number):
    document = document_loaded(browser, document_number)
    return document.find_element_by_tag_name(document_tag)


def get_table_rows(document_table):
    return document_table.find_elements_by_tag_name(table_row_tag)


def get_row_data(row):
    row_data = row.find_elements_by_tag_name(row_data_tag)
    return row_data[0].strip(), row_data[1].strip()


def record_value(row, title):
    row_title, row_content = get_row_data(row)
    if row_title == title:
        return row_content
    else:
        print(f'Encountered "{row_title}:{row_content}" when looking for {title}.')


def record_document(browser, document_number):
    document_table = document_table_data(browser, document_number)
    rows = get_table_rows(document_table)
    instrument_number = record_value(rows[0], "Instrument #")
