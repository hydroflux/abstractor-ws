from settings.file_management import multiple_documents_comment
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import (date_from_string, element_title_strip, four_character_padding,
                                        list_to_string, newline_split,
                                        print_list_by_index, timeout,
                                        title_strip)

from armadillo.armadillo_variables import (book_and_page_text,
                                           document_tables_tag, legal_text,
                                           legal_update, parties_midpoint_text,
                                           reception_number_prefix,
                                           related_documents_text,
                                           related_types,
                                           type_and_number_table_id)
from armadillo.validation import (validate_date, validate_reception_number,
                                  validate_volume_page,
                                  verify_results_page_loaded)


def locate_document_type_and_number_table(browser, document):
    try:
        type_and_number_table_present = EC.presence_of_element_located((By.ID, type_and_number_table_id))
        WebDriverWait(browser, timeout).until(type_and_number_table_present)
        type_and_number_table = browser.find_element_by_id(type_and_number_table_id)
        return type_and_number_table
    except TimeoutException:
        print(f'Browser timed out trying to access document type and number table for '
              f'{document.extrapolate_value()}, please review.')
        input()


def access_table_information(table):
    return newline_split(element_title_strip(table))


def get_document_type_and_number_fields(browser, document):
    type_and_number_table = locate_document_type_and_number_table(browser, document)
    return access_table_information(type_and_number_table)


def handle_document_type_and_number_text(document, document_type_and_number_text):
    type_and_number_pieces = document_type_and_number_text.split(' - ')
    if len(type_and_number_pieces) == 2:
        return type_and_number_pieces
    elif len(type_and_number_pieces) == 3:
        return (' - ').join(type_and_number_pieces[:2]), type_and_number_pieces[2]
    else:
        print(f'Browser is unable to parse document type and number for '
              f'{document.extrapolate_value()}, please review: \n'
              f'{print_list_by_index(type_and_number_pieces)}')
        input()


def handle_document_validation(document, reception_number=None, volume=None, page=None):
    if document.type == 'document_number' and reception_number is not None:
        return validate_reception_number(document, reception_number)
    elif document.type == 'volume_and_page' and reception_number is None:
        return validate_volume_page(document, volume, page)
    else:
        return True


def access_document_type_and_number(document, document_type_and_number_text):
    if handle_document_validation(document, reception_number=document_type_and_number_text):
        return handle_document_type_and_number_text(document, document_type_and_number_text)
    else:
        print(f'Browser failed to validate reception number for '
              f'{document.extrapolate_value()} instead finding '
              f'"{document_type_and_number_text}", please review before continuing...')
        input()


def access_download_value(document, reception_number):
    document.download_value = reception_number[len(reception_number_prefix):].replace('-', '_')


def access_reception_number(reception_number):
    return reception_number[len(reception_number_prefix):].replace('-', '')


def update_reception_number(document, reception_number):
    if reception_number.startswith(reception_number_prefix) and handle_document_validation(document, reception_number):
        access_download_value(document, reception_number)
        reception_number = access_reception_number(reception_number)
        if document.type == 'volume_and_page' and reception_number == '1':
            return (f'{four_character_padding(document.document_value()[0])}-'
                    f'{four_character_padding(document.document_value()[1])}')
        return reception_number
    else:
        print(f'Reception number "{reception_number}" does not match the expected result format for '
              f'{document.extrapolate_value()}, please review...')
        input()
        return reception_number


def handle_reception_number(dataframe, document, reception_number):
    reception_number = update_reception_number(document, reception_number)
    document.reception_number = reception_number
    dataframe['Reception Number'].append(reception_number)


def record_document_type_and_number(browser, dataframe, document):
    document_type_and_number_fields = get_document_type_and_number_fields(
        browser, document)
    document_type, reception_number = access_document_type_and_number(
        document, document_type_and_number_fields[0])
    dataframe['Document Type'].append(document_type)
    handle_reception_number(dataframe, document, reception_number)


def locate_document_information_tables(browser, document):
    try:
        information_tables_present = EC.presence_of_element_located((By.TAG_NAME, document_tables_tag))
        WebDriverWait(browser, timeout).until(information_tables_present)
        information_tables = browser.find_elements_by_tag_name(document_tables_tag)
        return information_tables
    except TimeoutException:
        print(f'Browser timed out trying to get document information tables for '
              f'{document.extrapolate_value()}, please review.')
        input()

# Substituted document_tables_class for document_tables_tag => testing for result solvency

# def locate_document_information_tables(browser, document):
#     try:
#         information_tables_present = EC.presence_of_element_located((By.CLASS_NAME, document_tables_class))
#         WebDriverWait(browser, timeout).until(information_tables_present)
#         information_tables = browser.find_elements_by_class_name(document_tables_class)
#         return information_tables
#     except TimeoutException:
#         print(f'Browser timed out trying to get document information tables for '
#               f'{document.extrapolate_value()}, please review.')
#         input()


def access_date(date_text, document, type):
    if validate_date(date_text):
        return date_from_string(date_text)
    else:
        print(f'Browser failed to validate {type} date for '
              f'{document.extrapolate_value()} instead finding '
              f'"{date_text}", recording an empty string instead.')
        return ''


def record_date(row, dataframe, document, type):
    date = access_date(title_strip(row), document, type)
    dataframe[f'{type.title()} Date'].append(date)


# Should this be 'access' instead of 'get'?
def get_book_volume_page_field(document_table):
    return document_table[document_table.index(book_and_page_text) + 1]


def access_book_volume_page(document_table):
    book_volume_page_field = get_book_volume_page_field(document_table)
    return (
        book_volume_page_field.split(' ')[0],
        book_volume_page_field.split(' ')[2],
        book_volume_page_field.split(' ')[4]
        )


def handle_book_volume_page(document_table, document):
    book, volume, page = access_book_volume_page(document_table)
    if handle_document_validation(document, volume=volume, page=page):
        return book, volume, page
    else:
        print(f'Browser failed to validate volume & page for '
              f'{document.extrapolate_value()}, instead finding '
              f'"Book: {book}, Volume: {volume}, Page: {page}", '
              f'please review before continuing...')
        input()
        return book, volume, page


def record_book_volume_page(document_table, dataframe, document):
    book, volume, page = handle_book_volume_page(document_table, document)
    dataframe["Book"].append(book)
    dataframe["Volume"].append(volume)
    dataframe["Page"].append(page)


def record_indexing_information(document_table, dataframe, document):
    record_date(document_table[3], dataframe, document, "recording")
    record_date(document_table[-1], dataframe, document, "effective")
    # recording_date = access_date(title_strip(document_table[3]), document, "recording")
    # document_date = access_date(title_strip(document_table[-1]), document, "document")
    # dataframe['Recording Date'].append(recording_date)
    # dataframe["Document Date"].append(document_date)
    record_book_volume_page(document_table, dataframe, document)
    # book, page = access_book_and_page(document_table)
    # dataframe["Book"].append(book)
    # dataframe["Page"].append(page)


def get_parties_midpoint(document_table):
    return document_table.index(parties_midpoint_text)


def access_parties_information(document_table):
    parties_midpoint = get_parties_midpoint(document_table)
    grantor = list(map(title_strip, (document_table[1:parties_midpoint])))
    grantee = list(map(title_strip, (document_table[(parties_midpoint + 1):])))
    return list_to_string(grantor), list_to_string(grantee)


def record_parties_information(document_table, dataframe):
    grantor, grantee = access_parties_information(document_table)
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


def legal_updates(legal, i=0):
    while i < len(legal_text):
        legal = legal.replace(legal_text[i], legal_update[i])
        i += 1
    return legal


def access_legal(legal_row):
    return legal_updates(legal_row.split('  ')[0])


def aggregate_legal_description(document_table):
    return list_to_string(list(map(access_legal, (document_table[1:]))))


def record_legal(document_table, dataframe):
    legal = aggregate_legal_description(document_table)
    dataframe['Legal'].append(legal)


def aggregate_document_table_information(browser, dataframe, document):
    document_tables = locate_document_information_tables(browser, document)
    record_indexing_information(newline_split(document_tables[1].text), dataframe, document)
    record_parties_information(access_table_information(document_tables[3]), dataframe)
    record_related_documents(newline_split(document_tables[6].text), dataframe)
    record_legal(newline_split(document_tables[8].text), dataframe)


def record_comments(dataframe, document):
    if document.number_results == 1:
        dataframe['Comments'].append('')
    elif document.number_results > 1:
        dataframe["Comments"].append(multiple_documents_comment(document))


def record_document_fields(browser, dataframe, document):
    record_document_type_and_number(browser, dataframe, document)
    aggregate_document_table_information(browser, dataframe, document)
    record_comments(dataframe, document)


def record(browser, dataframe, document):
    verify_results_page_loaded(browser, document)
    record_document_fields(browser, dataframe, document)
