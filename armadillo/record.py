from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import timeout

from armadillo.armadillo_variables import document_information_id, type_and_number_field_tag


def get_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_id(document_information_id)
        return document_information
    except TimeoutException:
        print(f'Browser timed out trying to access document information for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def get_type_and_number_field(document_information, document):
    try:
        type_and_number_field_present = EC.presence_of_element_located((By.TAG_NAME, type_and_number_field_tag))
        WebDriverWait(document_information, timeout).until(type_and_number_field_present)
        type_and_number_field = document_information.find_element_by_tag_name(type_and_number_field_tag)
        return type_and_number_field
    except TimeoutException:
        print(f'Browser timed out trying to get document type and reception number fields for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_document_type_and_reception_number(document_information, document):
    type_and_number_field = get_type_and_number_field(document_information, document)


def record_indexing_information(document_information, document):
    pass


def record_grantor(browser, document):
    pass


def record_grantee(browser, document):
    pass


def record_reception_number(browser, document):
    pass


def record_document_date(browser, document):
    pass


def record_recording_date(browser, document):
    pass


def record_legal(browser, document):
    pass


def record_related_documents(browser, document):
    pass


def record_comments(browser, document):
    pass


def aggregate_document_information(browser, dataframe, document):
    document_information = get_document_information(browser, document)


def record_document_fields(browser, county, dataframe, document):
    pass


def record(browser, county, dataframe, document):
    pass
