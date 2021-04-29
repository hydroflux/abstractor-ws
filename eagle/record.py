from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)

from settings.file_management import extrapolate_document_value
from settings.general_functions import scroll_to_top, scroll_into_view
from settings.settings import long_timeout, search_errors, timeout

from eagle.eagle_variables import (document_information_id,
                                   document_table_class, index_table_tags,
                                   information_links_class, less_info,
                                   loading_status, missing_values, more_info,
                                   pdf_viewer_load_id, related_table_class)


def pdf_load_status(browser):
    try:
        pdf_viewer_loaded = EC.presence_of_element_located((By.ID, pdf_viewer_load_id))
        WebDriverWait(browser, long_timeout).until(pdf_viewer_loaded)
        return browser.find_element_by_id(pdf_viewer_load_id).text
    except TimeoutException:
        print("Browser timed out while waiting for the PDF Viewer to load.")


def wait_for_pdf_to_load(browser):
    while pdf_load_status(browser).startswith(loading_status):
        sleep(0.5)
        pdf_load_status(browser)


def access_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_info = browser.find_element_by_id(document_information_id)
        return document_info.find_elements_by_class_name(document_table_class)
    except TimeoutException:
        print(f'Browser timed out while trying to access document information for '
              f'{extrapolate_document_value(document)}.')


def display_all_information(browser):
    document_info = browser.find_element_by_id(document_information_id)
    information_links = document_info.find_elements_by_class_name(information_links_class)
    for link in information_links:
        if link.text == more_info:
            scroll_into_view(browser, link)
            link.click()


def drop_superfluous_information(string):
    if string.endswith(less_info):
        return string[:-len(less_info)]
    else:
        return string


def access_table_body(document_table):
    return document_table.find_element_by_tag_name(index_table_tags[0])


def access_table_rows(table_body):
    body_text = table_body.find_elements_by_tag_name(index_table_tags[1])
    return body_text


def access_title_case_text(data):
    return data.text.title().replace("'S ", "'s ")


def access_field_body_no_title(field_info):
    return "\n".join(field_info.text.split("\n")[1:])


def access_field_body(field_info):
    return "\n".join(field_info.text.split("\n")[1:]).title()


def access_indexing_information(document_table):
    table_body = access_table_body(document_table)
    table_rows = access_table_rows(table_body)
    return map(access_field_body, table_rows)


def record_document_type(document_table, dataframe):
    document_type = document_table.text.title().replace("'S ", "'s ")
    dataframe["Document Type"].append(document_type)


def split_reception_field(reception_field):
    if "Book" in reception_field and "Page" in reception_field:
        reception_fields = reception_field.split("\n")
        reception_number = reception_fields[0]
        book = reception_fields[2]
        page = reception_fields[4]
    else:
        reception_number = reception_field
        book = search_errors[2]
        page = search_errors[2]
    return reception_number, book, page


def record_indexing_data(document_table, dataframe):
    reception_field, recording_date = access_indexing_information(document_table)
    reception_number, book, page = split_reception_field(reception_field)
    dataframe["Reception Number"].append(reception_number)
    dataframe["Book"].append(book)
    dataframe["Page"].append(page)
    dataframe["Recording Date"].append(recording_date[:10])
    return reception_number


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


def record_notes(document_tables, dataframe):
    try:
        notes = access_field_body_no_title(document_tables[5])
        if notes == search_errors[3] or notes == search_errors[4]:
            pass
        elif notes.startswith(search_errors[3]) or notes.startswith("$"):
            pass
        elif notes.endswith(search_errors[3]):
            pass
        else:
            notes = f'Notes: {notes}'
            if dataframe["Legal"][-1] == "":
                dataframe["Legal"][-1] = notes
            else:
                dataframe["Legal"][-1] = f'{dataframe["Legal"][-1]}\n{notes}'
    except IndexError:
        pass


def aggregate_document_information(document_tables, dataframe):
    reception_number = record_indexing_data(document_tables[1], dataframe)
    record_document_type(document_tables[0], dataframe)
    record_name_data(document_tables[2], dataframe)
    record_legal_data(document_tables[4], dataframe)
    record_related_documents(document_tables[-2], dataframe)
    record_notes(document_tables, dataframe)
    dataframe["Comments"].append("")
    return reception_number


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


def check_length(dataframe):
    grantors = len(dataframe["Grantor"])
    grantees = len(dataframe["Grantee"])
    books = len(dataframe["Book"])
    pages = len(dataframe["Page"])
    reception_numbers = len(dataframe["Reception Number"])
    document_types = len(dataframe["Document Type"])
    recording_dates = len(dataframe["Recording Date"])
    legals = len(dataframe["Legal"])
    related_documents = len(dataframe["Related Documents"])
    comments = len(dataframe["Comments"])
    if (grantors == grantees == books == pages == reception_numbers == document_types == recording_dates == legals == related_documents == comments):
        pass
    else:
        print("Grantors: ", grantors)
        print("Grantees: ", grantees)
        print("Books: ", books)
        print("Pages: ", pages)
        print("Reception Numbers: ", reception_numbers)
        print("Document Types: ", document_types)
        print("Recording Dates: ", recording_dates)
        print("Legals: ", legals)
        print("Related Documents: ", related_documents)
        print("Comments: ", comments)


def record_document_fields(browser, dataframe, document):
    document_tables = access_document_information(browser, document)
    display_all_information(browser)
    reception_number = aggregate_document_information(document_tables, dataframe)
    scroll_to_top(browser)
    return reception_number


# This series of functions may be unnecessary, continue to test
def review_entry(browser, dataframe, document):
    while dataframe["Grantor"][-1] == missing_values[0] and dataframe["Grantee"][-1] == missing_values[0]\
            and dataframe["Related Documents"][-1] == missing_values[1]:
        print("Recording of last document was processed incorrectly, attempting to record again.")
        re_record_document_fields(browser, dataframe, document)


def re_record_document_fields(browser, dataframe, document):
    drop_last_entry(dataframe)
    record_document_fields(browser, dataframe, document)


def record_document(browser, dataframe, document):
    wait_for_pdf_to_load(browser)
    document_number = record_document_fields(browser, dataframe, document)
    check_length(dataframe)
    review_entry(browser, dataframe, document)
    return document_number
