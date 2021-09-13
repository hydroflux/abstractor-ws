from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import date_from_string, get_field_value, timeout

from rattlesnake.validation import validate_date, validate_reception_number, verify_document_description_page_loaded
from rattlesnake.rattlesnake_variables import document_description_table_id, document_tables_tag, row_tag_name, row_data_tag_name, reception_number_id, volume_id, page_id, effective_date_id, recording_date_id, document_type_id, legal_id, empty_value_fields


# def locate_document_description_table(browser, document):
#     try:
#         document_description_table_present = EC.presence_of_element_located((By.ID, document_description_table_id))
#         WebDriverWait(browser, timeout).until(document_description_table_present)
#         document_description_table = browser.find_element_by_id(document_description_table_id)
#         return document_description_table
#     except TimeoutException:
#         print(f'Browser timed out trying to locate document description table for '
#               f'{extrapolate_document_value(document)}, please review.')
#         input()


# def locate_document_information_tables(document_description_table, document):
#     try:
#         information_tables_present = EC.presence_of_element_located((By.TAG_NAME, document_tables_tag))
#         WebDriverWait(document_description_table, timeout).until(information_tables_present)
#         information_tables = document_description_table.find_elements_by_tag_name(document_tables_tag)
#         return information_tables
#     except TimeoutException:
#         print(f'Browser timed out trying to get document information tables for '
#               f'{extrapolate_document_value(document)}, please review.')
#         input()


# def get_document_information_tables(browser, document):
#     document_description_table = locate_document_description_table(browser, document)
#     return locate_document_information_tables(document_description_table, document)


# def access_document_information_tables(browser, document):
#     return get_document_information_tables(browser, document)[2:]


# def locate_table_rows(table, document):
#     try:
#         table_rows_present = EC.presence_of_element_located((By.TAG_NAME, row_tag_name))
#         WebDriverWait(table, timeout).until(table_rows_present)
#         table_rows = table.find_elements_by_tag_name(row_tag_name)
#         return table_rows
#     except TimeoutException:
#         print(f'Browser timed out trying to locate table rows for '
#               f'{extrapolate_document_value(document)}, please review.')
#         input()


# def access_table_rows(table, document):
#     pass

def locate_information_field(browser, document, id, field_type):
    try:
        field_present = EC.presence_of_element_located((By.ID, id))
        WebDriverWait(browser, timeout).until(field_present)
        field = browser.find_element_by_id(id)
        return field
    except TimeoutException:
        print(f'Browser timed out trying to locate "{field_type}" field for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_field_value(browser, document, id, field_type):
    field = locate_information_field(browser, document, id, field_type)
    return get_field_value(field)


def record_field_value(dataframe, value, field_type):
    dataframe[f'{field_type.title()}'].append(value)


def record_reception_number(browser, dataframe, document, field_type='reception_number'):
    reception_number = access_field_value(browser, document, reception_number_id, field_type)
    if validate_reception_number(document, reception_number):
        record_field_value(dataframe, reception_number, field_type)


def record_null_value(dataframe, field_type):
    dataframe[f'{field_type.title()}'].append(empty_value_fields[-1])


def record_empty_value(dataframe, field_type):
    dataframe[f'{field_type.title()}'].append(empty_value_fields[0])


def record_volume(browser, dataframe, document, field_type='volume'):
    volume = access_field_value(browser, document, volume_id, field_type)
    if volume not in empty_value_fields:
        record_field_value(dataframe, volume, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_page(browser, dataframe, document, field_type='page'):
    page = access_field_value(browser, document, page_id, field_type)
    if page not in empty_value_fields:
        record_field_value(dataframe, page, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_effective_date(browser, dataframe, document, field_type='effective date'):
    effective_date = date_from_string(access_field_value(browser, document, effective_date_id, field_type))
    if validate_date(effective_date):
        record_field_value(dataframe, effective_date, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_recording_date(browser, dataframe, document, field_type='recording date'):
    recording_date = date_from_string(access_field_value(browser, document, recording_date_id, field_type).split()[0])
    if validate_date(recording_date):
        record_field_value(dataframe, recording_date, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_document_type(browser, dataframe, document):
    pass


def record_legal(browser, dataframe, document):
    pass


def record_grantor():
    pass


def record_grantee():
    pass


def record_parties_information():
    pass


def aggregate_party_information(browser, dataframe, document):
    pass
    # document_tables = access_document_information_tables(browser, document)
    # record_indexing_information(document_tables[0], dataframe, document)


def record_related_documents(dataframe):
    dataframe['Related Documents'].append('')


def record_comments(dataframe):
    dataframe['Comments'].append('')


def record_document_fields(browser, dataframe, document):
    aggregate_party_information(browser, dataframe, document)
    record_related_documents(dataframe)
    record_comments(dataframe)


def record(browser, dataframe, document):
    verify_document_description_page_loaded(browser, document)
    record_document_fields(browser, dataframe, document)
