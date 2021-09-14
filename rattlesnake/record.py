from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (date_from_string, element_title_strip,
                                        get_field_value, list_to_string,
                                        timeout, title_strip)

from rattlesnake.rattlesnake_variables import (document_type_id,
                                               effective_date_id,
                                               empty_value_fields,
                                               grantee_text, grantor_text,
                                               legal_id, page_id, parties_id,
                                               party_rows_tag_name,
                                               reception_number_id,
                                               recording_date_id,
                                               row_data_tag_name, volume_id)
from rattlesnake.validation import (validate_date, validate_reception_number, validate_volume_and_page_numbers,
                                    verify_document_description_page_loaded)


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
    if field_type.endswith('date'):
        return date_from_string(get_field_value(field))
    elif field_type == 'document type':
        return title_strip(get_field_value(field))
    else:
        return get_field_value(field)


def handle_document_type_verification(browser, document):
    if document.type == 'reception_number':
        reception_number = access_field_value(browser, document, reception_number_id, 'reception number')
        return validate_reception_number(document, reception_number)
    elif document.type == 'volume_and_page':
        page = access_field_value(browser, document, page_id, 'page')
        volume = access_field_value(browser, document, volume_id, 'volume')
        return validate_volume_and_page_numbers(document, volume, page)
    else:
        print(f'Document type "{document.type}" for "{document.value}" could not be validated, please review.')
        input()


def record_field_value(dataframe, value, field_type):
    dataframe[f'{field_type.title()}'].append(value)


def record_null_value(dataframe, field_type):
    dataframe[f'{field_type.title()}'].append(empty_value_fields[-1])


def record_empty_value(dataframe, field_type):
    dataframe[f'{field_type.title()}'].append(empty_value_fields[0])


def record_bad_value(dataframe, document, field_type, alt):
    if alt is None:
        print(f'No alternative trigger provided to record a bad value found in the '
              f'"{field_type}" field for "{extrapolate_document_value(document)}", please review')
        input()
    elif alt == 'empty':
        record_empty_value(dataframe, field_type)
    elif alt == 'null':
        record_null_value(dataframe, field_type)
    else:
        print(f'Encountered an unexpected problem trying to record a bad value found in the '
              f'"{field_type}" field for "{extrapolate_document_value(document)}" '
              f'with the alternative trigger "{alt}", please review.')
        input()


def check_dates(field_type, value):
    if field_type.endswith('date'):
        if validate_date(value):
            return True
    else:
        return True


def handle_value_content(dataframe, document, field_type, value, alt):
    if value not in empty_value_fields:
        if check_dates(field_type, value):
            record_field_value(dataframe, value, field_type)
        else:
            record_bad_value(dataframe, document, field_type, alt)
    elif value in empty_value_fields:
        record_bad_value(dataframe, document, field_type, alt)
    else:
        print(f'Encountered an issue with "{field_type}" field for '
              f'{extrapolate_document_value(document)}, which found a value of '
              f'"{value}" in the "{field_type}" field, please review.')
        input()


def record_value(browser, dataframe, document, field_type, id=None, value=None, alt=None):
    if value is None:
        value = access_field_value(browser, document, id, field_type)
    handle_value_content(dataframe, document, field_type, value, alt)


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


def record_parties_information(browser, dataframe, document):
    grantor, grantee = aggregate_party_information(browser, document)
    record_value(browser, dataframe, document, 'grantor', value=list_to_string(grantor), alt='empty')  # Grantor
    record_value(browser, dataframe, document, 'grantee', value=list_to_string(grantee), alt='empty')  # Grantee


def record_book(dataframe):
    dataframe['Book'].append('')


def record_related_documents(dataframe):
    dataframe['Related Documents'].append('')


def record_comments(dataframe):
    dataframe['Comments'].append('')


def record_document_fields(browser, dataframe, document):
    record_value(browser, dataframe, document, 'reception number', id=reception_number_id)  # Reception Number
    record_value(browser, dataframe, document, 'volume', id=volume_id, alt='null')  # Volume
    record_value(browser, dataframe, document, 'page', id=page_id, alt='null')  # Page
    record_value(browser, dataframe, document, 'effective date', id=effective_date_id, alt='empty')  # Effective Date
    record_value(browser, dataframe, document, 'recording date', id=recording_date_id, alt='empty')  # REcording Date
    record_value(browser, dataframe, document, 'document type', id=document_type_id)  # Document Type
    record_value(browser, dataframe, document, 'legal', id=legal_id, alt='null')  # Legal
    record_parties_information(browser, dataframe, document)  # Grantor / Grantee
    record_book(dataframe)  # Book
    record_related_documents(dataframe)  # Related Documents
    record_comments(dataframe)  # Comments


def record(browser, dataframe, document):
    if verify_document_description_page_loaded(browser, document):
        if handle_document_type_verification(browser, document):
            document.description_link = browser.current_url
            record_document_fields(browser, dataframe, document)
    # need to add else statement handlers
