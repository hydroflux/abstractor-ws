from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import date_from_string, element_title_strip, get_field_value, list_to_string, timeout, title_strip

from rattlesnake.validation import validate_date, validate_reception_number, verify_document_description_page_loaded
from rattlesnake.rattlesnake_variables import document_description_table_id, document_tables_tag, row_tag_name, row_data_tag_name, reception_number_id, volume_id, page_id, effective_date_id, recording_date_id, document_type_id, legal_id, empty_value_fields, parties_id, party_rows_tag_name, grantor_text, grantee_text


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


def record_reception_number(browser, dataframe, document, field_type='reception number'):
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


def record_document_type(browser, dataframe, document, field_type='document type'):
    document_type = access_field_value(browser, document, document_type_id, field_type)
    if document_type not in empty_value_fields:
        record_field_value(dataframe, title_strip(document_type), field_type)
    else:
        record_null_value(dataframe, field_type)


def record_legal(browser, dataframe, document, field_type='legal'):
    legal = access_field_value(browser, document, legal_id, field_type)
    if legal not in empty_value_fields:
        record_field_value(dataframe, legal, field_type)
    else:
        record_empty_value(dataframe, field_type)


def locate_parties_rows(parties_table, document):
    try:
        party_rows_present = EC.presence_of_element_located((By.TAG_NAME, party_rows_tag_name))
        WebDriverWait(parties_table, timeout).until(party_rows_present)
        party_rows = parties_table.find_elements_by_tag_name(party_rows_tag_name)
        return party_rows
    except TimeoutException:
        print(f'Browser timed out trying to locate document party rows for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_parties_rows(browser, document, field_type='parties'):
    parties_table = locate_information_field(browser, document, parties_id, field_type)
    return locate_parties_rows(parties_table, document)[1:]


def locate_row_data(row, document):
    try:
        row_data_present = EC.presence_of_element_located((By.TAG_NAME, row_data_tag_name))
        WebDriverWait(row, timeout).until(row_data_present)
        row_data = row.find_elements_by_tag_name(row_data_tag_name)
        return row_data
    except TimeoutException:
        print(f'Browser timed out trying to locate row data for '
              f'{extrapolate_document_value(document)} row "{row.text}", please review.')
        input()


def access_party_details(row_data, party_type, party_list):
    if row_data[0].text == party_type:
        party_list.append(element_title_strip(row_data[1]))


def map_party_information(rows, document):
    grantor = []
    grantee = []
    for row in rows:
        row_data = locate_row_data(row, document)
        access_party_details(row_data, grantor_text, grantor)
        access_party_details(row_data, grantee_text, grantee)
    return grantor, grantee


def aggregate_party_information(browser, document):
    rows = access_parties_rows(browser, document)
    return map_party_information(rows, document)


def record_grantor(dataframe, grantor, field_type='grantor'):
    if grantor not in empty_value_fields:
        record_field_value(dataframe, grantor, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_grantee(dataframe, grantee, field_type='grantee'):
    if grantee not in empty_value_fields:
        record_field_value(dataframe, grantee, field_type)
    else:
        record_empty_value(dataframe, field_type)


def record_parties_information(browser, dataframe, document):
    grantor, grantee = aggregate_party_information(browser, document)
    record_grantor(dataframe, list_to_string(grantor))
    record_grantee(dataframe, list_to_string(grantee))


def record_related_documents(dataframe):
    dataframe['Related Documents'].append('')


def record_comments(dataframe):
    dataframe['Comments'].append('')


def record_document_fields(browser, dataframe, document):
    record_reception_number(browser, dataframe, document)
    record_volume(browser, dataframe, document)
    record_page(browser, dataframe, document)
    record_effective_date(browser, dataframe, document)
    record_recording_date(browser, dataframe, document)
    record_legal(browser, dataframe, document)
    record_parties_information(browser, dataframe, document)
    record_related_documents(dataframe)
    record_comments(dataframe)


def record(browser, dataframe, document):
    verify_document_description_page_loaded(browser, document)
    record_document_fields(browser, dataframe, document)
