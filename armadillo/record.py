from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (date_from_string, element_title_strip,
                                        list_to_string, newline_split, timeout,
                                        title_strip)

from armadillo.armadillo_variables import (book_and_page_text,
                                           document_tables_class,
                                           party_midpoint_text,
                                           related_documents_text,
                                           related_types,
                                           type_and_number_table_id)
from armadillo.validation import validate_date, validate_reception_number


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


def access_date(date_text, document, type):
    if validate_date(date_text):
        return date_from_string(date_text)
    else:
        print(f'Browser failed to validate {type} date for '
              f'{extrapolate_document_value(document)} instead finding '
              f'"{date_text}", please review before continuing...')
        input()


def get_book_and_page_field(document_table):
    return document_table[document_table.index(book_and_page_text) + 1]


def access_book_and_page(document_table):
    book_and_page_field = get_book_and_page_field(document_table)
    return book_and_page_field.split(' ')[2], book_and_page_field.split(' ')[4]


def record_indexing_information(document_table, dataframe, document):
    recording_date = access_date(title_strip(document_table[3]), document, "recording")
    document_date = access_date(title_strip(document_table[-1]), document, "document")
    book, page = access_book_and_page(document_table)
    dataframe['Recording Date'].append(recording_date)
    dataframe["Document Date"].append(document_date)
    dataframe["Book"].append(book)
    dataframe["Page"].append(page)


def get_party_midpoint(document_table):
    return document_table.index(party_midpoint_text)


def access_party_information(document_table):
    party_midpoint = get_party_midpoint(document_table)
    grantor = list(map(title_strip, (document_table[1:party_midpoint])))
    grantee = list(map(title_strip, (document_table[(party_midpoint + 1):])))
    return list_to_string(grantor), list_to_string(grantee)


def record_party_information(document_table, dataframe):
    grantor, grantee = access_party_information(document_table)
    dataframe['Grantor'].append(grantor)
    dataframe['Grantee'].append(grantee)


def get_related_document_fields(document_table):
    return document_table[document_table.index(related_documents_text) + 1:]


def build_related_documents(related_string):
    related_document_array = []
    index = 0
    for element in related_string.split('  '):
        if element != '' and element != ' ':
            related_document_array.append(f'{related_types[index]}: {element}')
        index += 1
    return (', ').join(related_document_array)


def access_related_documents(related_documents_fields):
    return list_to_string(list(map(build_related_documents, related_documents_fields)))


def record_related_documents(document_table, dataframe):
    related_documents_fields = get_related_document_fields(document_table)
    related_documents = access_related_documents(related_documents_fields)
    dataframe['Related Documents'].append(related_documents)


def record_legal(browser, document):
    pass


def record_comments(browser, document):
    pass


def aggregate_document_information(browser, dataframe, document):
    record_document_type_and_number(browser, dataframe, document)
    document_tables = locate_document_information_tables(browser, document)
    record_indexing_information(access_table_information(document_tables[0]), dataframe, document)
    record_party_information(access_table_information(document_tables[1]), dataframe)
    record_related_documents(newline_split(document_tables[2].text), dataframe)


def record_document_fields(browser, county, dataframe, document):
    pass


def record(browser, county, dataframe, document):
    pass
