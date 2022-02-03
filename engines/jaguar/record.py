from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_elements_by_tag_name)
from serializers.recorder import record_comments, record_empty_values, record_value

from settings.general_functions import (date_from_string, list_to_string, title_strip,
                                        update_sentence_case_extras)

from engines.jaguar.validation import validate_reception_number


def get_document_type_and_number(browser, abstract, document):
    document_type_and_number_field = locate_element_by_id(browser, abstract.county.ids["Document Type And Number"],
                                                          "document type and number field", document=document)
    return document_type_and_number_field.text.split('\n')[0]


def access_document_type_and_number(browser, abstract, document):
    document_type_and_number = get_document_type_and_number(browser, abstract, document)
    return document_type_and_number.split(' - ')


def handle_reception_number(abstract, document):
    if validate_reception_number(document, document.reception_number):
        record_value(abstract, 'reception number', document.reception_number)
    else:
        print(f'Reception number "{document.reception_number}" does not match the expected value for '
              f'{document.extrapolate_value()}, please review and press enter to continue...')
        input()


def record_document_type_and_number(browser, abstract, document):
    document_type, reception_number = access_document_type_and_number(browser, abstract, document)
    document.reception_number = reception_number
    record_value(abstract, 'document type', update_sentence_case_extras(title_strip(document_type)))
    handle_reception_number(abstract, document)


def record_indexing_information(abstract, document_table, document):
    recording_date_field = locate_element_by_class_name(document_table, abstract.county.classes["Recording Date"],
                                                        "recording date", document=document)
    recording_date = date_from_string(recording_date_field.text[:10])
    record_value(abstract, 'recording date', recording_date)


def record_grantor(abstract, document_table, document):
    grantor_text = document_table.text.split('\n')[1:]
    grantor_list = list(map(title_strip, grantor_text))
    grantor = update_sentence_case_extras(list_to_string(grantor_list))
    record_value(abstract, 'grantor', grantor)


def record_grantee(abstract, document_table, document):
    grantee_text = document_table.text.split('\n')[1:]
    grantee_list = list(map(title_strip, grantee_text))
    grantee = update_sentence_case_extras(list_to_string(grantee_list))
    record_value(abstract, 'grantee', grantee)


def record_related_documents(abstract, document_table, document):
    related_documents_text = document_table.text.split('\n')[1:]
    related_documents_list = list(map(title_strip, related_documents_text))
    related_documents = list_to_string(related_documents_list)
    record_value(abstract, 'related documents', related_documents)


def record_legal(abstract, document_table, document):
    legal = title_strip(document_table.text)
    record_value(abstract, 'legal', legal)


def aggregate_document_table_information(browser, abstract, document):
    document_tables = locate_elements_by_tag_name(browser, abstract.county.tags["Document Tables"],
                                                  "document tables", document=document)
    record_indexing_information(abstract, document_tables[2], document)
    record_grantor(abstract, document_tables[6], document)
    record_grantee(abstract, document_tables[7], document)
    record_related_documents(abstract, document_tables[8], document)
    record_legal(abstract, document_tables[10], document)


def record(browser, abstract, document):
    record_document_type_and_number(browser, abstract, document)
    aggregate_document_table_information(browser, abstract, document)
    record_comments(abstract, document)
    record_empty_values(abstract, ['effective date', 'book', 'volume', 'page', 'document link'])
