from armadillo.validation import validate_date, validate_reception_number
from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import date_from_string, element_title_strip, newline_split, timeout, title_strip

from armadillo.armadillo_variables import document_information_id


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


def access_indexing_fields(document_information):
    return newline_split(element_title_strip(document_information))


def access_document_type_and_number(document_type_and_number_text, document):
    if validate_reception_number(document_type_and_number_text, document):
        return document_type_and_number_text.split(' - ')
    else:
        print(f'Browser failed to validate reception number for '
              f'{extrapolate_document_value(document)} instead finding '
              f'{document_type_and_number_text}, please review before continuing...')
        input()


def access_recording_date(recording_date_text, document):
    if validate_date(recording_date_text):
        return date_from_string(recording_date_text)
    else:
        print(f'Browser failed to validate recording date for '
              f'{extrapolate_document_value(document)} instead finding '
              f'"{recording_date_text}", please review before continuing...')
        input()


def record_indexing_information(document_information, dataframe, document):
    indexing_information_fields = access_indexing_fields(document_information)
    document_type, reception_number = access_document_type_and_number(indexing_information_fields[0], document)
    recording_date = access_recording_date(title_strip(indexing_information_fields[4]), document)


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
    record_indexing_information(document_information, dataframe, document)


def record_document_fields(browser, county, dataframe, document):
    pass


def record(browser, county, dataframe, document):
    pass
