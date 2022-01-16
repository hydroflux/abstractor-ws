from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.jaguar import document_type_and_number_field_id
from settings.general_functions import update_sentence_case_extras

from jaguar.validation import validate_reception_number


def get_document_type_and_number(browser, document):
    document_type_and_number_field = locate_element_by_id(browser, document_type_and_number_field_id,
                                                          "document type and number field", document=document)
    return document_type_and_number_field.text.split('\n')[0]


def access_document_type_and_number(browser, document):
    document_type_and_number = get_document_type_and_number(browser, document)
    return document_type_and_number.split(' - ')


def handle_reception_number(dataframe, document, reception_number):
    if validate_reception_number(reception_number, document):
        document.reception_number = reception_number
        dataframe['Reception Number'].append(reception_number)
    else:
        print(f'Reception number "{reception_number}" does not match the expected value for '
              f'{document.extrapolate_value()}, please review and press enter to continue...')
        input()


def record_document_type_and_number(browser, dataframe, document):
    document_type, reception_number = access_document_type_and_number(browser, document)
    document.reception_number = reception_number
    dataframe['Document Type'].append(update_sentence_case_extras(document_type))
    handle_reception_number(dataframe, document, reception_number)


def aggregate_document_table_information(browser, dataframe, document):
    pass


def record_comments(dataframe, document):
    pass


def record_document_link(dataframe, document):
    pass


def record(browser, dataframe, document):
    record_document_type_and_number(browser, dataframe, document)
    aggregate_document_table_information(browser, dataframe, document)
