from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.settings import not_applicable, timeout

from tiger.tiger_variables import (book_page_abbreviation, document_image_id,
                                   document_information_id, document_tag,
                                   empty_value, empty_values, row_data_tag,
                                   row_titles, table_row_tag)


def document_image_loaded(browser, document_number):
    try:
        document_image_present = EC.presence_of_element_located((By.ID, document_image_id))
        WebDriverWait(browser, timeout).until(document_image_present)
    except TimeoutException:
        print(f'Browser timed out while waiting for the document {document_number} image to load.')


def document_information_loaded(browser, document_number):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        return browser.find_element_by_id(document_information_id)
    except TimeoutException:
        print(f'Browser timed out while waiting for the document {document_number} information to load.')


def document_loaded(browser, document_number):
    document_image_loaded(browser, document_number)
    return document_information_loaded(browser, document_number)


def document_table_data(browser, document_number):
    document = document_loaded(browser, document_number)
    return document.find_element_by_tag_name(document_tag)


def get_table_rows(document_table):
    return document_table.find_elements_by_tag_name(table_row_tag)


def get_element_text(element):
    return element.text.strip()


def get_row_data(row):
    row_data = row.find_elements_by_tag_name(row_data_tag)
    return get_element_text(row_data[0]), get_element_text(row_data[1])


def get_row_value(row, title):
    row_title, row_content = get_row_data(row)
    if row_title == title:
        return row_content
    else:
        print(f'Encountered "{row_title}:{row_content}" when looking for {title}.')


def check_for_value(content, value_type):
    if content != empty_values[value_type]:
        return True


def record_instrument_number(dictionary, row):
    instrument_number = get_row_value(row, row_titles["reception_number"])
    dictionary["Reception Number"].append(instrument_number)


def record_book_and_page(dictionary, row):
    book_page_value = get_row_value(row, row_titles["book_and_page"])
    if book_page_value.startswith(book_page_abbreviation):
        book, page = book_page_value[len(book_page_abbreviation):].split("/")
        book = book.strip()
        page = page.strip()
        if book == '0' and page == '0':
            book = not_applicable
            page = not_applicable
        dictionary["Book"].append(book)
        dictionary["Page"].append(page)
    else:
        print(f'Encountered unexpected value "{book_page_value}" when trying to record book & page.')


def record_recording_date(dictionary, row):
    recording_date = get_row_value(row, row_titles["recording_date"])
    dictionary["Recording Date"].append(recording_date[:10])


def record_document_type(dictionary, row):
    document_type = get_row_value(row, row_titles["document_type"])
    dictionary["Document Type"].append(document_type.title())


def record_grantor(dictionary, row):
    grantor = get_row_value(row, row_titles["grantor"])
    dictionary["Grantor"].append(grantor.title())


def record_grantee(dictionary, row):
    grantee = get_row_value(row, row_titles["grantee"])
    dictionary["Grantee"].append(grantee.title())


def record_related_documents(dictionary, row):
    related_documents = get_row_value(row, row_titles["related_documents"])
    dictionary["Related Documents"].append(related_documents)


def record_legal(dictionary, row_1, row_2):
    legal = get_row_value(row_1, row_titles["legal"])
    additional_legal = get_row_value(row_2, row_titles["additional_legal"])
    if legal != additional_legal:
        dictionary["Legal"].append(f'{legal}\n{additional_legal}')
    else:
        dictionary["Legal"].append(legal)


# Write a function to check additional information for rows 4, 7
def record_document(browser, dictionary, document_number):
    document_table = document_table_data(browser, document_number)
    rows = get_table_rows(document_table)
    record_instrument_number(dictionary, rows[0])
    record_book_and_page(dictionary, rows[1])
    record_recording_date(dictionary, rows[2])
    record_document_type(dictionary, rows[5])
    record_grantor(dictionary, rows[7])
    record_grantee(dictionary, rows[8])
    record_related_documents(dictionary, rows[9])
    record_legal(dictionary, rows[10], rows[11])
    dictionary["Comments"].append(empty_value)
