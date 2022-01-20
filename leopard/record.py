from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.county_variables.leopard import (book_page_abbreviation,
                                               document_image_id,
                                               document_information_id,
                                               document_table_tag,
                                               next_result_id,
                                               previous_result_id,
                                               row_data_tag, row_titles,
                                               table_row_tag)
from settings.county_variables.general import not_applicable
from settings.general_functions import (get_element_text, scroll_to_top,
                                        timeout, title_strip)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)
# Script is similar to tiger but superior at time of testing--needs further review


def document_image_loaded(browser, document):
    try:
        document_image_present = EC.presence_of_element_located((By.ID, document_image_id))
        WebDriverWait(browser, timeout).until(document_image_present)
    except TimeoutException:
        print(f'Browser timed out waiting for '
              f'{extrapolate_document_value(document)} document image to load.')


def get_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_id(document_information_id)
        return document_information
    except TimeoutException:
        print(f'Browser timed out waiting for '
              f'{extrapolate_document_value(document)} document information to load.')


def document_loaded(browser, document):
    document_image_loaded(browser, document)
    return get_document_information(browser, document)


def get_document_table_data(browser, document_information, document):
    try:
        document_table_data_present = EC.presence_of_element_located((By.TAG_NAME, document_table_tag))
        WebDriverWait(browser, timeout).until(document_table_data_present)
        document_table_data = document_information.find_element_by_tag_name(document_table_tag)
        return document_table_data
    except TimeoutException:
        print(f'Browser timed out getting table data for '
              f'{extrapolate_document_value(document)}.')


# Used in crocodile without any edits
def get_table_rows(browser, document_table, document):
    try:
        table_rows_present = EC.presence_of_element_located((By.TAG_NAME, table_row_tag))
        WebDriverWait(browser, timeout).until(table_rows_present)
        table_rows = document_table.find_elements_by_tag_name(table_row_tag)
        return table_rows
    except TimeoutException:
        print(f'Browser timed out getting table rows for '
              f'{extrapolate_document_value(document)}.')


def get_document_content(browser, document):
    document_information = document_loaded(browser, document)
    document_table = get_document_table_data(browser, document_information, document)
    return get_table_rows(browser, document_table, document)


def get_row_data(row):
    row_data = row.find_elements_by_tag_name(row_data_tag)
    return get_element_text(row_data[0]), get_element_text(row_data[1])


# Copied & audited in crocodile
def check_rows(rows, title):
    for row in rows:
        try:
            row_title, row_content = get_row_data(row)
            if row_title == title:
                if row_content != "":
                    return row_content
                else:
                    return not_applicable
        except IndexError:
            continue
    return not_applicable


# Function designed to help with development, no production purpose
def row_title_check(rows):
    for row in rows:
        try:
            row_title, row_content = get_row_data(row)
            print(rows.index(row), "row_title", row_title, "row content", row_content)
        except IndexError:
            continue


# Pull this out, removed during crocodile development (don't see the purpose
# )
# def locate_reception_number(rows):
#     return check_rows(rows, row_titles["reception_number"])

def record_reception_number(rows, dictionary):
    # reception_number = locate_reception_number(rows)
    reception_number = check_rows(rows, row_titles["reception_number"])
    dictionary["Reception Number"].append(reception_number)
    return reception_number


def record_book_and_page(rows, dictionary):
    book_and_page = check_rows(rows, row_titles["book_and_page"])
    if book_and_page == not_applicable:
        dictionary["Book"].append(book_and_page)
        dictionary["Page"].append(book_and_page)
    else:
        if book_and_page.startswith(book_page_abbreviation):
            book_and_page = book_and_page[len(book_page_abbreviation):]
        book, page = book_and_page.replace("/", "").split()
        if book == "0":
            dictionary["Book"].append(not_applicable)
        else:
            dictionary["Book"].append(book)
        if page == "0":
            dictionary["Page"].append(not_applicable)
        else:
            dictionary["Page"].append(page)


def record_recording_date(rows, dictionary):
    recording_date = check_rows(rows, row_titles["recording_date"])
    dictionary["Recording Date"].append(recording_date[:10])


def record_document_type(rows, dictionary):
    document_type = check_rows(rows, row_titles["document_type"])
    dictionary["Document Type"].append(title_strip(document_type))


def record_grantor(rows, dictionary):
    grantor = check_rows(rows, row_titles["grantor"])
    dictionary["Grantor"].append(title_strip(grantor))


def record_grantee(rows, dictionary):
    grantee = check_rows(rows, row_titles["grantee"])
    dictionary["Grantee"].append(title_strip(grantee))


def record_related_documents(rows, dictionary):
    related_documents = check_rows(rows, row_titles["related_documents"])
    alt_related_documents = check_rows(rows, row_titles["alt_related_documents"])
    if related_documents == not_applicable and alt_related_documents == not_applicable:
        dictionary["Related Documents"].append("")
    else:
        if related_documents == alt_related_documents or alt_related_documents == not_applicable:
            dictionary["Related Documents"].append(related_documents)
        elif related_documents == not_applicable:
            dictionary["Related Documents"].append(alt_related_documents)
        else:
            combined_related_documents = f'{related_documents}\n{alt_related_documents}'
            dictionary["Related Documents"].append(combined_related_documents)


def record_legal(rows, dictionary):
    legal = check_rows(rows, row_titles["legal"])
    alt_legal = check_rows(rows, row_titles["alt_legal"])
    if legal == not_applicable and alt_legal == not_applicable:
        dictionary["Legal"].append("")
    else:
        if legal == alt_legal or alt_legal == not_applicable:
            dictionary["Legal"].append(legal)
        elif legal == not_applicable:
            dictionary["Legal"].append(alt_legal)
        else:
            combined_legal = f'{legal}\n{alt_legal}'
            dictionary["Legal"].append(combined_legal)


#  Extrapolate this to a generalized file
def record_comments(county, dictionary, document):
    if document.number_results > 1:
        dictionary["Comments"].append(f'Multiple documents located at {extrapolate_document_value(document)}'
                                      f' on the {county} recording website; Each of the {document.number_results}'
                                      f' documents has been listed, please review')
    else:
        dictionary["Comments"].append("")


def aggregate_document_information(browser, county, document, dictionary, rows):
    document_number = record_reception_number(rows, dictionary)
    record_book_and_page(rows, dictionary)
    record_recording_date(rows, dictionary)
    record_document_type(rows, dictionary)
    record_grantor(rows, dictionary)
    record_grantee(rows, dictionary)
    record_related_documents(rows, dictionary)
    record_legal(rows, dictionary)
    record_comments(county, dictionary, document)
    return document_number


def get_previous_result_button(browser, document):
    try:
        previous_result_button_present = EC.element_to_be_clickable((By.ID, previous_result_id))
        WebDriverWait(browser, timeout).until(previous_result_button_present)
        previous_result_button = browser.find_element_by_id(previous_result_id)
        return previous_result_button
    except TimeoutException:
        print(f'Browser timed out trying to locate previous result button for '
              f'{extrapolate_document_value(document)}')


def previous_result(browser, document):
    previous_result_button = get_previous_result_button(browser, document)
    scroll_to_top(browser)
    previous_result_button.click()


def get_next_result_button(browser, document):
    try:
        next_result_button_present = EC.element_to_be_clickable((By.ID, next_result_id))
        WebDriverWait(browser, timeout).until(next_result_button_present)
        next_result_button = browser.find_element_by_id(next_result_id)
        return next_result_button
    except TimeoutException:
        print(f'Browser timed out trying to locate next result button for '
              f'{extrapolate_document_value(document)}')


def next_result(browser, document):
    next_result_button = get_next_result_button(browser, document)
    scroll_to_top(browser)
    next_result_button.click()


# def get_reception_number(browser, document):
#     rows = get_document_content(browser, document)
#     return locate_reception_number(rows)


def record_document(browser, county, dictionary, document):
    rows = get_document_content(browser, document)
    document_number = aggregate_document_information(browser, county, document, dictionary, rows)
    return document_number
