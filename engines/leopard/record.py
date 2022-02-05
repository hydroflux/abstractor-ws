from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_tag_name,
                                         locate_elements_by_tag_name)

from serializers.recorder import record_comments, record_value

from settings.county_variables.general import not_applicable
from settings.general_functions import get_element_text, title_strip

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)


def access_document_information(browser, abstract, document):
    locate_element_by_id(browser, abstract.county.ids["Document Image"], "document image", False, document)  # Wait for image to load
    document_information = locate_element_by_id(browser, abstract.county.ids["Document Information"],
                                                "document information", False, document)
    return document_information


def get_document_content(browser, abstract, document):
    document_information = access_document_information(browser, abstract, document)
    document_table_data = locate_element_by_tag_name(document_information, abstract.county.tags["Document Table"],
                                                     "document table data", False, document)
    table_rows = locate_elements_by_tag_name(document_table_data, abstract.county.tags["Table Rows"], "table rows", False, document)
    return table_rows


def get_row_data(abstract, row):
    row_data = row.find_elements_by_tag_name(abstract.county.tags["Row Data"])
    return get_element_text(row_data[0]), get_element_text(row_data[1])


# Copied & audited in crocodile
def check_rows(abstract, rows, title):
    for row in rows:
        try:
            row_title, row_content = get_row_data(abstract, row)
            if row_title == title:
                if row_content != "":
                    return row_content
                else:
                    return not_applicable
        except IndexError:
            continue
    return not_applicable


def access_reception_number(abstract, document, rows):
    reception_number = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["reception_number"])
    document.reception_number = reception_number


def record_book_and_page(abstract, rows):
    book_and_page = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["book_and_page"])
    if book_and_page == 'N/A':
        record_value(abstract, 'book', '')
        record_value(abstract, 'page', '')
    else:
        if book_and_page.startswith(abstract.county.other["Abbreviation"]):
            book_and_page = book_and_page[len(abstract.county.other["Abbreviation"]):]
        book, page = book_and_page.replace("/", "").split()
        if book == '0' and page == '0':
            record_value(abstract, 'book', '')
            record_value(abstract, 'page', '')
        else:
            record_value(abstract, 'book', book)
            record_value(abstract, 'page', page)


def record_recording_date(abstract, rows):
    recording_date = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["recording_date"])
    record_value(abstract, 'recording date', recording_date[:10])


def record_document_type(abstract, rows):
    document_type = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["document_type"])
    record_value(abstract, 'document type', title_strip(document_type))


def record_grantor(abstract, rows):
    grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["grantor"])
    record_value(abstract, 'grantor', title_strip(grantor))


def record_grantee(abstract, rows):
    grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["grantee"])
    record_value(abstract, 'grantee', title_strip(grantee))


def record_related_documents(abstract, rows):
    related_documents = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["related_documents"])
    alt_related_documents = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["alt_related_documents"])
    if related_documents == not_applicable and alt_related_documents == not_applicable:
        record_value(abstract, 'related documents', '')
    else:
        if related_documents == alt_related_documents or alt_related_documents == not_applicable:
            record_value(abstract, 'related documents', related_documents)
        elif related_documents == not_applicable:
            record_value(abstract, 'related documents', alt_related_documents)
        else:
            combined_related_documents = f'{related_documents}\n{alt_related_documents}'
            record_value(abstract, 'related documents', combined_related_documents)


def record_legal(abstract, rows):
    legal = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["legal"])
    alt_legal = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["alt_legal"])
    if legal == not_applicable and alt_legal == not_applicable:
        record_value(abstract, 'legal', '')
    else:
        if legal == alt_legal or alt_legal == not_applicable:
            record_value(abstract, 'legal', legal)
        elif legal == not_applicable:
            record_value(abstract, 'legal', alt_legal)
        else:
            combined_legal = f'{legal}\n{alt_legal}'
            record_value(abstract, 'legal', combined_legal)


def aggregate_document_information(abstract, document, rows):
    access_reception_number(abstract, document, rows)
    record_value(abstract, 'reception number', document.reception_number)
    record_book_and_page(abstract, rows)
    record_recording_date(abstract, rows)
    record_document_type(abstract, rows)
    record_grantor(abstract, rows)
    record_grantee(abstract, rows)
    record_related_documents(abstract, rows)
    record_legal(abstract, rows)
    record_comments(abstract, document, rows)


def record(browser, abstract, document):
    if not abstract.review:
        rows = get_document_content(browser, abstract, document)
        if abstract.download_only:
            access_reception_number(abstract, document, rows)
        else:
            aggregate_document_information(abstract, document, rows)
