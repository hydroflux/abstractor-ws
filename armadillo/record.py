from armadillo.validation import validate_date, validate_reception_number
from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import date_from_string, element_title_strip, newline_split, timeout, title_strip

from armadillo.armadillo_variables import type_and_number_table_id, document_tables_class


def locate_document_type_and_number_table(browser, document):
    try:
        type_and_number_table_present = EC.presence_of_element_located((By.ID, type_and_number_table_id))
        WebDriverWait(browser, timeout).until(type_and_number_table_present)
        type_and_number_table = browser.find_element_by_id(type_and_number_table_id)
        return type_and_number_table
    except TimeoutException:
        print(f'Browser timed out trying to access document type and number table for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_table_information(table):
    return newline_split(element_title_strip(table))


def get_document_type_and_number_fields(browser, document):
    type_and_number_table = locate_document_type_and_number_table(browser, document)
    return access_table_information(type_and_number_table)


def access_document_type_and_number(document_type_and_number_text, document):
    if validate_reception_number(document_type_and_number_text, document):
        return document_type_and_number_text.split(' - ')
    else:
        print(f'Browser failed to validate reception number for '
              f'{extrapolate_document_value(document)} instead finding '
              f'{document_type_and_number_text}, please review before continuing...')
        input()


def record_document_type_and_number(document_information, dataframe, document):
    document_type_and_number_fields = get_document_type_and_number_fields(
        document_information)
    document_type, reception_number = access_document_type_and_number(
        document_type_and_number_fields[0], document)
    dataframe['Reception Number'].append(reception_number)
    dataframe['Document Type'].append(document_type)


def locate_document_information_tables(browser, document):
    try:
        information_tables_present = EC.presence_of_element_located((By.CLASS_NAME, document_tables_class))
        WebDriverWait(browser, timeout).until(information_tables_present)
        information_tables = browser.find_elements_by_class_name(document_tables_class)
        return information_tables
    except TimeoutException:
        print(f'Browser timed out trying to get document information tables for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_recording_date(recording_date_text, document):
    if validate_date(recording_date_text):
        return date_from_string(recording_date_text)
    else:
        print(f'Browser failed to validate recording date for '
              f'{extrapolate_document_value(document)} instead finding '
              f'"{recording_date_text}", please review before continuing...')
        input()


def record_indexing_information(document_table, dataframe, document):
    recording_date = access_recording_date(title_strip(document_table[3]), document)
    dataframe['Recording Date'].append(recording_date)
    # dataframe["Book"].append(book)
    # dataframe["Page"].append(page)
    # dataframe["Document Date"].append(document_date)


def record_grantor(browser, document):
    pass


def record_grantee(browser, document):
    pass


def record_legal(browser, document):
    pass


def record_related_documents(browser, document):
    pass


def record_comments(browser, document):
    pass


def aggregate_document_information(browser, dataframe, document):
    record_document_type_and_number(browser, dataframe, document)
    document_tables = locate_document_information_tables(browser, document)
    record_indexing_information(access_table_information(document_tables[0]), dataframe, document)


def record_document_fields(browser, county, dataframe, document):
    pass


def record(browser, county, dataframe, document):
    pass
