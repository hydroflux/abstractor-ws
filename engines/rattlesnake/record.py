from engines.rattlesnake.validation import (
    validate_date, validate_reception_number, validate_volume_and_page_numbers,
    verify_document_description_page_loaded)

from selenium_utilities.inputs import get_field_value
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_elements_by_tag_name)

from settings.county_variables.rattlesnake import (document_type_id,
                                                   effective_date_id,
                                                   empty_value_fields,
                                                   grantee_text, grantor_text,
                                                   legal_id, page_id,
                                                   parties_id,
                                                   party_rows_tag_name,
                                                   reception_number_id,
                                                   recording_date_id,
                                                   row_data_tag_name,
                                                   volume_id)
from settings.dataframe_management import multiple_documents_comment
from settings.general_functions import (date_from_string, element_title_strip,
                                        list_to_string, title_strip,
                                        update_sentence_case_extras)


def access_field_value(browser, document, id, field_type):
    field = locate_element_by_id(browser, id, field_type, document=document)
    if field_type.endswith('date'):
        return date_from_string(get_field_value(field).split(' ')[0])
    elif field_type == 'document type':
        return update_sentence_case_extras(title_strip(get_field_value(field)))
    else:
        if field_type == 'reception number':
            document.reception_number = get_field_value(field)
        return get_field_value(field)


def handle_document_type_verification(browser, document):
    if document.type == 'document_number':
        reception_number = access_field_value(browser, document, reception_number_id, 'reception number')
        return validate_reception_number(document, reception_number)
    elif document.type == 'volume_and_page':
        page = access_field_value(browser, document, page_id, 'page')
        volume = access_field_value(browser, document, volume_id, 'volume')
        return validate_volume_and_page_numbers(document, volume, page)
    else:
        print(f'Document type "{document.type}" for "{document.value}" could not be validated, please review.')
        input()


def record_field_value(abstract, value, field_type):
    abstract.dataframe[f'{field_type.title()}'].append(value)


def record_invalid_value(abstract, document, field_type, alt):
    if alt is None:
        print(f'No alternative trigger provided to record a bad value found in the '
              f'"{field_type}" field for "{document.extrapolate_value()}", please review')
        input()
    elif alt == 'empty':
        record_field_value(abstract, empty_value_fields[0], field_type)
    elif alt == 'null':
        record_field_value(abstract, empty_value_fields[1], field_type)
    else:
        print(f'Encountered an unexpected problem trying to record a bad value found in the '
              f'"{field_type}" field for "{document.extrapolate_value()}" '
              f'with the alternative trigger "{alt}", please review.')
        input()


def check_dates(field_type, value):
    if field_type.endswith('date'):
        if validate_date(value):
            return True
    else:
        return True


def handle_value_content(abstract, document, field_type, value, alt):
    if value not in empty_value_fields:
        if check_dates(field_type, value):
            record_field_value(abstract, value, field_type)
        else:
            record_invalid_value(abstract, document, field_type, alt)
    elif value in empty_value_fields:
        record_invalid_value(abstract, document, field_type, alt)
    else:
        print(f'Encountered an issue with "{field_type}" field for '
              f'{document.extrapolate_value()}, which found a value of '
              f'"{value}" in the "{field_type}" field, please review.')
        input()


def record_value(browser, abstract, document, field_type, id=None, value=None, alt=None):
    if value is None:
        value = access_field_value(browser, document, id, field_type)
    handle_value_content(abstract, document, field_type, value, alt)


def access_parties_rows(browser, document, field_type='parties'):
    parties_table = locate_element_by_id(browser, parties_id, field_type, document=document)
    return locate_elements_by_tag_name(parties_table, party_rows_tag_name, "document party rows", document=document)[1:]


def access_party_details(row_data, party_type, party_list):
    if row_data[0].text == party_type:
        party_list.append(element_title_strip(row_data[1]))


def map_party_information(rows, document):
    grantor = []
    grantee = []
    for row in rows:
        row_data = locate_elements_by_tag_name(row, row_data_tag_name, f'row data => {row.text}', document=document)
        # row_data = locate_row_data(row, document)
        access_party_details(row_data, grantor_text, grantor)
        access_party_details(row_data, grantee_text, grantee)
    return grantor, grantee


def aggregate_party_information(browser, document):
    rows = access_parties_rows(browser, document)
    return map_party_information(rows, document)


def record_parties_information(browser, abstract, document):
    grantor, grantee = aggregate_party_information(browser, document)
    record_value(browser, abstract, document, 'grantor',
                 value=update_sentence_case_extras(list_to_string(grantor)), alt='empty')  # Grantor
    record_value(browser, abstract, document, 'grantee',
                 value=update_sentence_case_extras(list_to_string(grantee)), alt='empty')  # Grantee


def record_book(abstract):
    abstract.dataframe['Book'].append('')


def record_related_documents(abstract):
    abstract.dataframe['Related Documents'].append('')


def record_comments(abstract, document):
    if document.number_results == 1:
        abstract.dataframe['Comments'].append('')
    elif document.number_results > 1:
        abstract.dataframe["Comments"].append(multiple_documents_comment(document))


def record_document_fields(browser, abstract, document):
    record_value(browser, abstract, document, 'reception number', id=reception_number_id)  # Reception Number
    record_value(browser, abstract, document, 'volume', id=volume_id, alt='null')  # Volume
    record_value(browser, abstract, document, 'page', id=page_id, alt='null')  # Page
    record_value(browser, abstract, document, 'effective date', id=effective_date_id, alt='empty')  # Effective Date
    record_value(browser, abstract, document, 'recording date', id=recording_date_id, alt='empty')  # Recording Date
    record_value(browser, abstract, document, 'document type', id=document_type_id, alt='null')  # Document Type
    record_value(browser, abstract, document, 'legal', id=legal_id, alt='null')  # Legal
    record_parties_information(browser, abstract, document)  # Grantor / Grantee
    record_book(abstract)  # Book
    record_related_documents(abstract)  # Related Documents
    record_comments(abstract, document)  # Comments


def record(browser, abstract, document):
    if verify_document_description_page_loaded(browser, document):
        if handle_document_type_verification(browser, document):
            document.description_link = browser.current_url
            record_document_fields(browser, abstract, document)
    # need to add else statement handlers
