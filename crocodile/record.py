from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import not_applicable
from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, get_element_text,
                                        timeout, title_strip)

from crocodile.crocodile_variables import (document_information_class,
                                           document_title,
                                           general_information_id, grantee_id,
                                           grantor_id, legal_id,
                                           related_documents_id)


def locate_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.CLASS_NAME, document_information_class))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_class_name(document_information_class)
        return document_information
    except TimeoutException:
        print(f'Browser timed out trying to locate document page information for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_general_information(document_information, document):
    try:
        general_information_present = EC.presence_of_element_located((By.ID, general_information_id))
        WebDriverWait(document_information, timeout).until(general_information_present)
        general_information = document_information.find_element_by_id(general_information_id)
        return general_information
    except TimeoutException:
        print(f'Browser timed out trying to locate general information for '
              f'{extrapolate_document_value(document)}')


def record_general_information(document_information, document):
    general_information = locate_general_information(document_information, document)
    print(general_information)


def locate_document_table(browser, document, table_id, type):
    try:
        document_table_present = EC.presence_of_element_located((By.ID, table_id))
        WebDriverWait(browser, timeout).until(document_table_present)
        document_table = browser.find_element_by_id(table_id)
        return document_table
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} document table for '
              f'{extrapolate_document_value(document)}, please review.')


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


def record_legal_information(browser, dictionary, document):
    legal_table = locate_document_table(browser, document, legal_id, "legal information")
    legal = title_strip(join_column_without_title(legal_table))
    dictionary["Legal"].append(legal)
    # Need to create a way to handle multiple pages of legal
    print("legal", legal)


def record_related_document_information(browser, dictionary, document):
    pass


def aggregate_document_information(browser, dictionary, document):
    record_grantor_information(browser, dictionary, document)
    record_grantee_information(browser, dictionary, document)
    record_legal_information(browser, dictionary, document)
    record_related_document_information(browser, dictionary, document)


def record_document(browser, county, dictionary, document):
    assert_window_title(browser, document_title)
    document_information = locate_document_information(browser, document)
    document_number = record_general_information(document_information, document)
    aggregate_document_information(browser, dictionary, document)
    return document_number
