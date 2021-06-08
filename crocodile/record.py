from selenium.common.exceptions import (NoSuchElementException,
                                        NoSuchWindowException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import not_applicable
from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, get_element_text,
                                        timeout, title_strip, zipped_list)

from crocodile.crocodile_variables import (additional_legal_pages_class, row_titles,
                                           document_information_class,
                                           document_title, row_header_tag,
                                           general_information_id, grantee_id,
                                           grantor_id, legal_id,
                                           related_documents_id, row_data_tag,
                                           table_row_tag)

# def locate_document_information(browser, document):
#     try:
#         document_information_present = EC.presence_of_element_located((By.CLASS_NAME, document_information_class))
#         WebDriverWait(browser, timeout).until(document_information_present)
#         document_information = browser.find_element_by_class_name(document_information_class)
#         return document_information
#     except TimeoutException:
#         print(f'Browser timed out trying to locate document page information for '
#               f'{extrapolate_document_value(document)}, please review.')


def locate_general_information(document_information, document):
    try:
        general_information_present = EC.presence_of_element_located((By.ID, general_information_id))
        WebDriverWait(document_information, timeout).until(general_information_present)
        general_information = document_information.find_element_by_id(general_information_id)
        return general_information
    except TimeoutException:
        print(f'Browser timed out trying to locate general information for '
              f'{extrapolate_document_value(document)}')


def locate_document_table(browser, document, table_id, type):
    try:
        document_table_present = EC.presence_of_element_located((By.ID, table_id))
        WebDriverWait(browser, timeout).until(document_table_present)
        document_table = browser.find_element_by_id(table_id)
        return document_table
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} document table for '
              f'{extrapolate_document_value(document)}, please review.')


# Stripped straight from leopard
def get_table_rows(browser, document_table, document):
    try:
        table_rows_present = EC.presence_of_element_located((By.TAG_NAME, table_row_tag))
        WebDriverWait(browser, timeout).until(table_rows_present)
        table_rows = document_table.find_elements_by_tag_name(table_row_tag)
        return table_rows
    except TimeoutException:
        print(f'Browser timed out getting table rows for '
              f'{extrapolate_document_value(document)}.')


# This could be a generalized function
def get_row_data(row, tag):
    return row.find_elements_by_tag_name(tag)


def get_general_information_data(browser, general_information_table, document):
    general_information_rows = get_table_rows(browser, general_information_table, document)
    headers = get_row_data(general_information_rows[0], row_header_tag)
    data = get_row_data(general_information_rows[1], row_data_tag)
    return zipped_list(headers, data)


# Copied & audited from leopard
def check_list_elements(general_information, title):
    for header, data in general_information:
        if header == title:
            if data != "":
                return data
            else:
                return not_applicable


def record_reception_number(general_information, dictionary):
    reception_number = check_list_elements(general_information, row_titles["reception_number"])
    dictionary["Reception Number"].append(reception_number)
    return reception_number


def record_book_and_page(general_information, dictionary):
    book_and_page = check_list_elements(general_information, row_titles["book_and_page"])
    if book_and_page == not_applicable:
        dictionary["Book"].append(book_and_page)
        dictionary["Page"].append(book_and_page)
    else:
        book, page = book_and_page.replace("/", "").split()
        if book == "0":
            dictionary["Book"].append(not_applicable)
        else:
            dictionary["Book"].append(book)
        if page == "0":
            dictionary["Page"].append(not_applicable)
        else:
            dictionary["Page"].append(page)


def record_document_type(general_information, dictionary):
    document_type = check_list_elements(general_information, row_titles["document_type"])
    if document_type == not_applicable:
        document_type = check_list_elements(general_information, row_titles["alt_document_type"])
    dictionary["Document Type"].append(title_strip(document_type))


def record_recording_date(general_information, dictionary):
    recording_date = check_list_elements(general_information, row_titles["recording_date"])
    dictionary["Recording Date"].append(recording_date[:10])


def record_general_information(browser, dictionary, document):
    general_information_table = locate_document_table(browser, document, general_information_id, "general information")
    general_information = get_general_information_data(browser, general_information_table, document)
    document_number = record_reception_number(general_information, dictionary)
    record_book_and_page(general_information, dictionary)
    record_document_type(general_information, dictionary)
    record_recording_date(general_information, dictionary)
    print(general_information)
    return document_number


def join_column_without_title(string):
    return '\n'.join(string.text.split('\n')[1:])


def record_grantor_information(browser, dictionary, document):
    grantor_table = locate_document_table(browser, document, grantor_id, "grantor")
    grantor = title_strip(join_column_without_title(grantor_table))
    dictionary["Grantor"].append(grantor)
    print("grantor", grantor)


def record_grantee_information(browser, dictionary, document):
    grantee_table = locate_document_table(browser, document, grantee_id, "grantee")
    grantee = title_strip(join_column_without_title(grantee_table))
    dictionary["Grantee"].append(grantee)
    print("grantee", grantee)


def get_number_legal_pages(legal_table):
    try:
        legal_pages = legal_table.find_element_by_class_name(additional_legal_pages_class).text
        return int(legal_pages[(legal_pages.rfind(" ") + 1):])
    except NoSuchElementException:
        return 1


def handle_legal_tables(legal_table):
    number_pages = get_number_legal_pages(legal_table)
    if number_pages == 1:
        return title_strip(join_column_without_title(legal_table))
    else:
        # Need to create a way to handle multiple pages of legal
        pass


def record_legal_information(browser, dictionary, document):
    legal_table = locate_document_table(browser, document, legal_id, "legal information")
    legal = handle_legal_tables(legal_table)
    print("legal", legal)
    dictionary["Legal"].append(legal)


def record_related_document_information(browser, dictionary, document):
    pass


def aggregate_document_information(browser, dictionary, document):
    record_grantor_information(browser, dictionary, document)
    record_grantee_information(browser, dictionary, document)
    record_legal_information(browser, dictionary, document)
    record_related_document_information(browser, dictionary, document)


def record_document(browser, county, dictionary, document):
    assert_window_title(browser, document_title)
    # document_information = locate_document_information(browser, document)
    document_number = record_general_information(browser, document)
    aggregate_document_information(browser, dictionary, document)
    return document_number
