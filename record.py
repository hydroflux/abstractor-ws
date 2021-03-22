from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import document_information_id, document_table_class, index_table_tags, related_table_class, bad_search_messages

def access_document_information(browser, document_number):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_info = browser.find_element_by_id(document_information_id)
        return document_info.find_elements_by_class_name(document_table_class)
    except TimeoutException:
        print(f'Browser timed out while trying to access document information for document number {document_number}.')

def access_table_body(document_table):
    return document_table.find_element_by_tag_name(index_table_tags[0])

def access_table_rows(table_body):
    return table_body.find_elements_by_tag_name(index_table_tags[1])

def access_title_case_text(data):
    return data.text.title()

def access_field_body(field_info):
    return field_info.text.split("\n")[1].title()

def access_indexing_information(document_table):
    table_body = access_table_body(document_table)
    table_rows = access_table_rows(table_body)
    return map(access_field_body, table_rows)

def record_document_type(document_table, dataframe):
    document_type = document_table.text.title()
    dataframe["Document Type"].append(document_type)

def record_indexing_data(document_table, dataframe):
    reception_number, recording_date = access_indexing_information(document_table)
    dataframe["Reception Number"].append(reception_number)
    dataframe["Recording Date"].append(recording_date)

def record_name_data(document_table, dataframe):
    grantor, grantee = access_indexing_information(document_tables[2])
    dataframe["Grantor"].append(grantor)
    dataframe["Grantee"].append(grantee)

def record_legal_data(document_table, dataframe):
    table_rows = access_table_rows(document_table)
    legal_data = table_rows[0].find_elements_by_tag_name(index_table_tags[2])
    legal = legal_data[-1].text
    dataframe["Legal"].append(legal)

def record_notes(document_table, dataframe):
    notes = access_field_body(document_tables[5])
    dataframe["Notes"].append(notes)

def record_related_documents(document_table, dataframe):
    related_table_rows = document_table.find_elements_by_class_name(related_table_class)
    related_documents_info = list(map(access_table_body, related_table_rows))
    related_document_list = list(map(access_title_case_text, related_documents_info))
    related_documents = "\n".join(related_document_list)
    dataframe["Related Documents"].append(related_documents)

def aggregate_document_information(document_tables, dataframe):
    record_document_type(document_tables[0], dataframe)
    record_indexing_data(document_tables[1], dataframe)
    record_name_data(document_tables[2], dataframe)
    record_legal_data(document_tables[4], dataframe)
    record_notes(document_tables[5], dataframe)
    record_related_documents(document_tables[6], dataframe)
    book, page = "N/A"
    dataframe["Book"].append(book)
    dataframe["Page"].append(page)
    dataframe["Comments"].append("")

def record_document(browser, dataframe, document_number):
    document_tables = access_document_information(browser, document_number)
    aggregate_document_information(document_tables, dataframe)

def record_bad_search(dataframe, document_number):
    dataframe["Grantor"].append(bad_search_messages[0])
    dataframe["Grantee"].append(bad_search_messages[0])
    dataframe["Book"].append(bad_search_messages[2])
    dataframe["Page"].append(bad_search_messages[2])
    dataframe["Reception Number"].append(document_number)
    dataframe["Document Type"].append(bad_search_messages[0])
    dataframe["Recording Date"].append(bad_search_messages[1])
    dataframe["Legal"].append(bad_search_messages[2])
    dataframe["Notes"].append(bad_search_messages[2])
    dataframe["Related Documents"].append(bad_search_messages[2])
    dataframe["Comments"].append(bad_search_messages[3])