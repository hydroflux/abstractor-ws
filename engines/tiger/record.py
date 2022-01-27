from selenium_utilities.locators import locate_element_by_id, locate_element_by_tag_name

from settings.county_variables.general import empty_value, not_applicable
from settings.county_variables.tiger import (book_page_abbreviation,
                                             document_image_id, search_script,
                                             document_information_id,
                                             document_table_tag, row_data_tag,
                                             row_titles, table_row_tag)
from settings.general_functions import get_element_text, javascript_script_execution, naptime

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)


def access_document_information(browser, document):
    locate_element_by_id(browser, document_image_id,  # Document Image Loaded
                         "document image", False, document)
    document_information = locate_element_by_id(browser, document_information_id,  # Document Information Loaded
                                                "document information", False, document)
    return document_information


def access_document_table_data(browser, document):
    document_information = access_document_information(browser, document)
    table_data = locate_element_by_tag_name(document_information, document_table_tag, "table data", False, document)
    return table_data


def get_table_rows(document_table):
    return document_table.find_elements_by_tag_name(table_row_tag)


def get_row_data(row):
    row_data = row.find_elements_by_tag_name(row_data_tag)
    return get_element_text(row_data[0]), get_element_text(row_data[1])


def get_row_value(row, title):
    row_title, row_content = get_row_data(row)
    if row_title == title:
        return row_content
    else:
        print(f'Encountered "{row_title}:{row_content}" when looking for {title}.')


def record_instrument_number(abstract, row):
    instrument_number = get_row_value(row, row_titles["reception_number"])
    abstract.dataframe["Reception Number"].append(instrument_number)


def record_book_and_page(abstract, row):
    book_page_value = get_row_value(row, row_titles["book_and_page"])
    if book_page_value.startswith(book_page_abbreviation):
        book, page = book_page_value[len(book_page_abbreviation):].split("/")
        book = book.strip()
        page = page.strip()
        if book == '0' and page == '0':
            book = not_applicable
            page = not_applicable
        abstract.dataframe["Book"].append(book)
        abstract.dataframe["Page"].append(page)
    elif book_page_value == '':
        abstract.dataframe["Book"].append(empty_value)
        abstract.dataframe["Page"].append(empty_value)
    else:
        print(f'Encountered unexpected value "{book_page_value}" when trying to record book & page.')


def record_recording_date(abstract, row):
    recording_date = get_row_value(row, row_titles["recording_date"])
    abstract.dataframe["Recording Date"].append(recording_date[:10])


def record_document_type(abstract, row):
    document_type = get_row_value(row, row_titles["document_type"])
    abstract.dataframe["Document Type"].append(document_type.title())


def record_grantor(abstract, row):
    grantor = get_row_value(row, row_titles["grantor"])
    abstract.dataframe["Grantor"].append(grantor.title())


def record_grantee(abstract, row):
    grantee = get_row_value(row, row_titles["grantee"])
    abstract.dataframe["Grantee"].append(grantee.title())


def record_related_documents(abstract, row):
    related_documents = get_row_value(row, row_titles["related_documents"])
    abstract.dataframe["Related Documents"].append(related_documents)


def record_legal(abstract, row_1):
    legal = get_row_value(row_1, row_titles["legal"])
    # additional_legal = get_row_value(row_2, row_titles["additional_legal"])
    # if legal != additional_legal:
    #     abstract.dataframe["Legal"].append(f'{legal}\n{additional_legal}')
    # else:
    abstract.dataframe["Legal"].append(legal)


# Write a function to check additional information for rows 4, 7
def record(browser, abstract, document):
    document_table = access_document_table_data(browser, document)
    rows = get_table_rows(document_table)
    record_instrument_number(abstract, rows[0])
    record_book_and_page(abstract, rows[1])
    record_recording_date(abstract, rows[2])
    record_document_type(abstract, rows[5])
    record_grantor(abstract, rows[7])
    record_grantee(abstract, rows[8])
    record_related_documents(abstract, rows[9])
    record_legal(abstract, rows[10])
    abstract["Comments"].append(empty_value)
    if abstract.download and document.image_available and not abstract.review:
        # These (below) are messy--need to move / update (duplicated in the download script)
        javascript_script_execution(search_script)
        naptime()
