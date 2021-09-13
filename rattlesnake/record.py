from settings.file_management import extrapolate_document_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import timeout

from rattlesnake.validation import verify_document_description_page_loaded
from rattlesnake.rattlesnake_variables import document_description_table_id, document_tables_tag, row_tag_name, row_data_tag_name, reception_number_id, volume_id, page_id, effective_date_id, recording_date_id, document_type_id, legal_id


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

def locate_reception_number():
    pass


def record_reception_number():
    pass


def locate_volume():
    pass


def record_volume():
    pass


def locate_page():
    pass


def record_page():
    pass


def locate_effective_date():
    pass


def record_effective_date():
    pass


def locate_recording_date():
    pass


def record_recording_date():
    pass


# def record_indexing_information(table, dataframe, document):
#     rows = locate_table_rows(table, document)
#     record_location_information(rows[0], dataframe, document)
#     record_date_information(rows[1], dataframe, document)


def locate_document_type():
    pass


def record_document_type():
    pass


def locate_legal():
    pass


def record_legal():
    pass


def record_grantor():
    pass


def record_grantee():
    pass


def record_parties_information():
    pass


def aggregate_party_information(browser, dataframe, document):
    pass
    # document_tables = access_document_information_tables(browser, document)
    # record_indexing_information(document_tables[0], dataframe, document)


def record_related_documents(dataframe):
    dataframe['Related Documents'].append('')


def record_comments(dataframe):
    dataframe['Comments'].append('')


def record_document_fields(browser, dataframe, document):
    aggregate_party_information(browser, dataframe, document)
    record_related_documents(dataframe)
    record_comments(dataframe)


def record(browser, dataframe, document):
    verify_document_description_page_loaded(browser, document)
    record_document_fields(browser, dataframe, document)
