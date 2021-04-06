from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# if __name__ == '__main__':
from settings.settings import search_errors, timeout

from eagle.eagle_variables import (document_information_id,
                                    document_table_class, index_table_tags,
                                    information_links_class, less_info,
                                    missing_values, more_info,
                                    related_table_class)
# else:
#     from ..settings.settings import search_errors, timeout
#     from .eagle_variables import (document_information_id,
#                                   document_table_class, index_table_tags,
#                                   information_links_class, less_info,
#                                   missing_values, more_info,
#                                   related_table_class)


def access_document_information(browser, document_number):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_info = browser.find_element_by_id(document_information_id)
        return document_info.find_elements_by_class_name(document_table_class)
    except TimeoutException:
        print(f'Browser timed out while trying to access document information for document number {document_number}.')


def display_all_information(browser):
    document_info = browser.find_element_by_id(document_information_id)
    information_links = document_info.find_elements_by_class_name(information_links_class)
    for link in information_links:
        if link.text == more_info:
            browser.execute_script("arguments[0].scrollIntoView();", link)
            link.click()


def drop_superfluous_information(string):
    if string.endswith(less_info):
        return string[:-len(less_info)]
    else:
        return string


def access_table_body(document_table):
    return document_table.find_element_by_tag_name(index_table_tags[0])


def access_table_rows(table_body):
    return table_body.find_elements_by_tag_name(index_table_tags[1])


def access_title_case_text(data):
    return data.text.title()


def access_field_body(field_info):
    return "\n".join(field_info.text.split("\n")[1:]).title()


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
    dataframe["Recording Date"].append(recording_date[:10])


def record_name_data(document_table, dataframe):
    grantor, grantee = access_indexing_information(document_table)
    dataframe["Grantor"].append(drop_superfluous_information(grantor))
    dataframe["Grantee"].append(drop_superfluous_information(grantee))


def record_legal_data(document_table, dataframe):
    table_rows = access_table_rows(document_table)
    legal_data = table_rows[1].find_elements_by_tag_name(index_table_tags[2])
    if legal_data == []:
        dataframe["Legal"].append(search_errors[2])
    else:
        legal = legal_data[-1].text
        dataframe["Legal"].append(legal)


def record_related_documents(document_table, dataframe):
    related_table_rows = document_table.find_elements_by_class_name(related_table_class)
    related_documents_info = list(map(access_table_body, related_table_rows))
    related_document_list = list(map(access_title_case_text, related_documents_info))
    related_documents = "\n".join(related_document_list)
    dataframe["Related Documents"].append(related_documents)


def record_notes(document_table, dataframe):
    notes = access_field_body(document_table)
    if dataframe["Legal"][-1] == "":
        dataframe["Legal"][-1] = notes
        dataframe["Comments"].append("")
    elif dataframe["Related Documents"][-1] == "":
        dataframe["Related Documents"][-1] = notes
        dataframe["Comments"].append("")
    else:
        dataframe["Comments"].append(notes)


def aggregate_document_information(document_tables, dataframe):
    record_document_type(document_tables[0], dataframe)
    record_indexing_data(document_tables[1], dataframe)
    record_name_data(document_tables[2], dataframe)
    record_legal_data(document_tables[4], dataframe)
    record_related_documents(document_tables[-2], dataframe)
    record_notes(document_tables[5], dataframe)
    book = search_errors[2]
    dataframe["Book"].append(book)
    page = search_errors[2]
    dataframe["Page"].append(page)


def drop_last_entry(dataframe):
    dataframe["Grantor"].pop()
    dataframe["Grantee"].pop()
    dataframe["Book"].pop()
    dataframe["Page"].pop()
    dataframe["Reception Number"].pop()
    dataframe["Document Type"].pop()
    dataframe["Recording Date"].pop()
    dataframe["Legal"].pop()
    dataframe["Related Documents"].pop()
    dataframe["Comments"].pop()


def scroll_to_top(browser):
    try:
        head_element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
        WebDriverWait(browser, timeout).until(head_element_present)
        head_element = browser.find_element_by_tag_name("body")
        browser.execute_script("arguments[0].scrollIntoView();", head_element)
    except TimeoutException:
        print("Timed out while trying to scroll to the top of the page.")


def record_document_fields(browser, dataframe, document_number):
    document_tables = access_document_information(browser, document_number)
    display_all_information(browser)
    aggregate_document_information(document_tables, dataframe)
    scroll_to_top(browser)

# This series of functions may be unnecessary, continue to test
def review_entry(browser, dataframe, document_number):
    while dataframe["Grantor"][-1] == missing_values[0] and dataframe["Grantee"][-1] == missing_values[0]\
            and dataframe["Related Documents"][-1] == missing_values[1]:
        print("Recording of last document was processed incorrectly, attempting to record again.")
        re_record_document_fields(browser, dataframe, document_number)


def re_record_document_fields(browser, dataframe, document_number):
    drop_last_entry(dataframe)
    record_document_fields(browser, dataframe, document_number)


def record_document(browser, dataframe, document_number):
    record_document_fields(browser, dataframe, document_number)
    review_entry(browser, dataframe, document_number)
