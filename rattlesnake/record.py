from settings.file_management import extrapolate_document_value
from rattlesnake.validation import verify_document_description_page_loaded
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import timeout

from rattlesnake.rattlesnake_variables import document_description_table_id, document_tables_tag


def locate_document_description_table(browser, document):
    try:
        document_description_table_present = EC.presence_of_element_located((By.ID, document_description_table_id))
        WebDriverWait(browser, timeout).until(document_description_table_present)
        document_description_table = browser.find_element_by_id(document_description_table_id)
        return document_description_table
    except TimeoutException:
        print(f'Browser timed out trying to locate document description table for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def locate_document_information_tables(document_description_table, document):
    try:
        information_tables_present = EC.presence_of_element_located((By.TAG_NAME, document_tables_tag))
        WebDriverWait(document_description_table, timeout).until(information_tables_present)
        information_tables = document_description_table.find_elements_by_tag_name(document_tables_tag)
        return information_tables
    except TimeoutException:
        print(f'Browser timed out trying to get document information tables for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def get_document_information_tables(browser, document):
    document_description_table = locate_document_description_table(browser, document)
    return locate_document_information_tables(document_description_table, document)


def access_document_information_tables(browser, document):
    return get_document_information_tables(browser, document)[2:]

def record_grantor():
    pass


def record_grantee():
    pass


def record_book():
    pass


def record_page():
    pass


def record_reception_number():
    pass


def record_document_type():
    pass


def record_effective_date():
    pass


def record_recording_date():
    pass


def record_legal():
    pass


def record_related_documents():
    pass


def record_comments():
    pass


def aggregate_document_information(browser, document):
    document_tables = access_document_information_tables(browser, document)


def record_document_fields():
    pass


def record(browser, document):
    verify_document_description_page_loaded(browser, document)