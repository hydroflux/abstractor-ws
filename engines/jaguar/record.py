from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_elements_by_tag_name)

from settings.county_variables.jaguar import (
    document_tables_tag, document_type_and_number_field_id,
    recording_date_field_class)
from settings.file_management import document_found, multiple_documents_comment
from settings.general_functions import (date_from_string, list_to_string, title_strip,
                                        update_sentence_case_extras)

from engines.jaguar.validation import validate_reception_number


def get_document_type_and_number(browser, document):
    document_type_and_number_field = locate_element_by_id(browser, document_type_and_number_field_id,
                                                          "document type and number field", document=document)
    return document_type_and_number_field.text.split('\n')[0]


def access_document_type_and_number(browser, document):
    document_type_and_number = get_document_type_and_number(browser, document)
    return document_type_and_number.split(' - ')


def handle_reception_number(dataframe, document, reception_number):
    if validate_reception_number(document, reception_number):
        document.reception_number = reception_number
        dataframe['Reception Number'].append(reception_number)
    else:
        print(f'Reception number "{reception_number}" does not match the expected value for '
              f'{document.extrapolate_value()}, please review and press enter to continue...')
        input()


def record_document_type_and_number(browser, dataframe, document):
    document_type, reception_number = access_document_type_and_number(browser, document)
    document.reception_number = reception_number
    dataframe['Document Type'].append(update_sentence_case_extras(title_strip(document_type)))
    handle_reception_number(dataframe, document, reception_number)


def record_indexing_information(document_table, dataframe, document):
    recording_date_field = locate_element_by_class_name(document_table, recording_date_field_class,
                                                        "recording date", document=document)
    recording_date = date_from_string(recording_date_field.text[:10])
    dataframe['Recording Date'].append(recording_date)
    dataframe['Effective Date'].append('')
    dataframe['Book'].append('N/A')
    dataframe['Volume'].append('')
    dataframe['Page'].append('N/A')


def record_parties_information(document_tables, dataframe, document):
    grantor_text = document_tables[6].text.split('\n')[1:]
    grantee_text = document_tables[7].text.split('\n')[1:]
    grantor_list = list(map(title_strip, grantor_text))
    grantee_list = list(map(title_strip, grantee_text))
    grantor = update_sentence_case_extras(list_to_string(grantor_list))
    grantee = update_sentence_case_extras(list_to_string(grantee_list))
    dataframe['Grantor'].append(grantor)
    dataframe['Grantee'].append(grantee)


def record_related_documents(document_table, dataframe, document):
    related_documents_text = document_table.text.split('\n')[1:]
    related_documents_list = list(map(title_strip, related_documents_text))
    related_documents = list_to_string(related_documents_list)
    dataframe['Related Documents'].append(related_documents)


def record_legal(document_table, dataframe, document):
    legal = title_strip(document_table.text)
    dataframe['Legal'].append(legal)


def aggregate_document_table_information(browser, dataframe, document):
    document_tables = locate_elements_by_tag_name(browser, document_tables_tag,
                                                  "document tables", document=document)
    record_indexing_information(document_tables[2], dataframe, document)
    record_parties_information(document_tables, dataframe, document)
    record_related_documents(document_tables[8], dataframe, document)
    record_legal(document_tables[10], dataframe, document)


def record_comments(dataframe, document):
    if document.number_results == 1:
        dataframe['Comments'].append('')
    elif document.number_results > 1:
        dataframe["Comments"].append(multiple_documents_comment(document))


def record_document_link(dataframe, document):
    dataframe['Document Link'].append('')


def record(browser, abstract, document):
    record_document_type_and_number(browser, abstract.dataframe, document)
    aggregate_document_table_information(browser, abstract.dataframe, document)
    record_comments(abstract.dataframe, document)
    record_document_link(abstract.dataframe, document)
    document_found(abstract, document)