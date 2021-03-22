from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import document_information_id, document_table_class, index_table_tags, related_table_class

def access_document_information(browser):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_info = browser.find_element_by_id(document_information_id)
        return document_info.find_elements_by_class_name(document_table_class)
    except TimeoutException:
        print("Browser timed out while trying to access document information.")

def access_table_body(document_table):
    return document_table.find_element_by_tag_name(index_table_tags[0])

def access_table_rows(table_body):
    return table_body.find_elements_by_tag_name(index_table_tags[1])

def return_title_text(data):
    return data.text.title()

def record_document_type(document_table):
    return document_table.text.title()

def record_field_body(field_info):
    return field_info.text.split("\n")[1].title()

def record_indexing_information(document_table):
    table_body = access_table_body(document_table)
    table_rows = access_table_rows(table_body)
    return map(record_field_body, table_rows)

def record_legal_data(document_table):
    table_rows = access_table_rows(document_table)
    legal_data = table_rows[0].find_elements_by_tag_name(index_table_tags[2])
    return legal_data[-1].text

def record_related_documents(document_table):
    related_table_rows = document_table.find_elements_by_class_name(related_table_class)
    related_documents_info = list(map(access_table_body, related_table_rows))
    related_document_list = list(map(return_title_text, related_documents_info))
    return "\n".join(related_document_list)

def aggregate_document_information(document_tables):
    document_type = record_document_type(document_tables[0])
    document_number, recording_date = record_indexing_information(document_tables[1])
    grantor, grantee = record_indexing_information(document_tables[2])
    legal = record_legal_data(document_tables[4])
    notes = record_field_body(document_tables[5])
    related_documents = record_related_documents(document_tables[6])

def store_document_information(document_dataframe):
    pass

def record_document(browser, document_dataframe):
    document_tables = access_document_information(browser)
    aggregate_document_information(document_tables)