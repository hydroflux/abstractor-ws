from selenium_utilities.locators import locate_element_by_id, locate_element_by_tag_name, locate_elements_by_tag_name

from serializers.recorder import record_comments, record_empty_values, record_value

from settings.county_variables.general import not_applicable
from settings.general_functions import get_element_text

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)


def access_document_information(browser, abstract, document):
    locate_element_by_id(browser, abstract.county.ids["Document Image"],  # Document Image Loaded
                         "document image", False, document)
    # doesn't work, need to test with throttling
    document_information = locate_element_by_id(browser, abstract.county.ids["Document Information"],
                                                "document information", False, document)  # Document Information Loaded
    return document_information


# def access_document_table_data(browser, abstract, document):
#     document_information = access_document_information(browser, abstract, document)
#     table_data = locate_element_by_tag_name(document_information, abstract.county.tags["Data"],
#                                             "table data", False, document)
#     return table_data


# def get_table_rows(abstract, document_table):
#     return document_table.find_elements_by_tag_name(abstract.county.tags["Rows"])


def get_document_content(browser, abstract, document):
    document_information = access_document_information(browser, abstract, document)
    document_table_body = locate_element_by_tag_name(document_information, abstract.county.tags["Body"],
                                                     "document table body", False, document)
    table_rows = locate_elements_by_tag_name(document_table_body, abstract.county.tags["Rows"],
                                             "document table rows", False, document)
    return table_rows


def get_row_data(abstract, row):
    row_data = row.find_elements("tag name", abstract.county.tags["Data"])
    return get_element_text(row_data[0]), get_element_text(row_data[1])


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


def record_reception_number(abstract, row, document):
    reception_number = check_rows(abstract, row, abstract.county.titles["Row Titles"]["reception_number"])
    document.reception_number = reception_number
    record_value(abstract, 'reception number', reception_number)


def record_book_and_page(abstract, row):
    book_page_value = check_rows(abstract, row, abstract.county.titles["Row Titles"]["book_and_page"])
    if book_page_value == not_applicable:
        record_value(abstract, 'book', not_applicable)
        record_value(abstract, 'page', not_applicable)
    else:
        if book_page_value.startswith(abstract.county.other["Abbreviation"]):
            book, page = book_page_value[len(abstract.county.other["Abbreviation"]):].split("/")
            book = book.strip()
            page = page.strip()
            if book == '0' and page == '0':
                book = not_applicable
                page = not_applicable
            record_value(abstract, 'book', book)
            record_value(abstract, 'page', page)
        elif book_page_value == '':
            record_value(abstract, 'book', not_applicable)
            record_value(abstract, 'page', not_applicable)
        else:
            # Below seems unnecessary, check with testing
            print(f'Encountered unexpected value "{book_page_value}" when trying to record book & page.')


def set_download_target_name(abstract, document):
    if document.reception_number == not_applicable:
        book = abstract.dataframe["Book"][-1].zfill(4)
        page = abstract.dataframe["Page"][-1].zfill(4)
        document.target_name = f'{document.county.prefix}-{book}-{page}.pdf'
        document.target_type == "book_and_page"
    else:
        document.target_name = f'{document.county.prefix}-{document.reception_number}.pdf'
        document.target_type = "document_number"


def record_recording_date(abstract, rows):
    recording_date = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["recording_date"])
    record_value(abstract, 'recording date', recording_date[:10])


def record_document_type(abstract, rows):
    document_type = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["document_type"])
    record_value(abstract, 'document type', document_type.title())


def record_grantor(abstract, rows):
    grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["grantor"])
    if grantor == not_applicable:
        grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["alt_grantor"])
        if grantor == not_applicable:
            grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["second_alt_grantor"])
            if grantor == not_applicable:
                grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["third_alt_grantor"])
                if grantor == not_applicable:
                    grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["fourth_alt_grantor"])
                    if grantor == not_applicable:
                        grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["fifth_alt_grantor"])
                        if grantor == not_applicable:
                            grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["sixth_alt_grantor"])
                            if grantor == not_applicable:
                                grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["seventh_alt_grantor"])
                                if grantor == not_applicable:
                                    grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["eighth_alt_grantor"])
                                    if grantor == not_applicable:
                                        grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["nineth_alt_grantor"])
                                        if grantor == not_applicable:
                                            grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["tenth_alt_grantor"])
                                            if grantor == not_applicable:
                                                grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["eleventh_alt_grantor"])
                                                if grantor == not_applicable:
                                                    grantor = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["twelfth_alt_grantor"])
    record_value(abstract, 'grantor', grantor.title())


def record_grantee(abstract, rows):
    grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["grantee"])
    if grantee == not_applicable:
        grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["alt_grantee"])
        if grantee == not_applicable:
            grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["second_alt_grantee"])
            if grantee == not_applicable:
                grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["third_alt_grantee"])
                if grantee == not_applicable:
                    grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["fourth_alt_grantee"])
                    if grantee == not_applicable:
                        grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["fifth_alt_grantee"])
                        if grantee == not_applicable:
                            grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["sixth_alt_grantee"])
                            if grantee == not_applicable:
                                grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["seventh_alt_grantee"])
                                if grantee == not_applicable:
                                    grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["eighth_alt_grantee"])
                                    if grantee == not_applicable:
                                        grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["nineth_alt_grantee"])
                                        if grantee == not_applicable:
                                            grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["tenth_alt_grantee"])
                                            if grantee == not_applicable:
                                                grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["eleventh_alt_grantee"])
                                                if grantee == not_applicable:
                                                    grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["twelfth_alt_grantee"])
                                                    if grantee == not_applicable:
                                                        grantee = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["thirteenth_alt_grantee"])
    record_value(abstract, 'grantee', grantee.title())


def record_related_documents(abstract, rows):
    related_documents = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["related_documents"])
    record_value(abstract, 'related documents', related_documents)


def record_legal(abstract, rows):
    legal = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["legal"])
    additional_legal = check_rows(abstract, rows, abstract.county.titles["Row Titles"]["additional_legal"])
    if additional_legal != not_applicable:
        if legal == not_applicable:
            legal = additional_legal
        elif additional_legal != legal:
            legal = f'{legal}\n{additional_legal}'
    record_value(abstract, 'legal', legal)


def aggregate_document_information(abstract, rows, document):
    record_reception_number(abstract, rows, document)
    record_book_and_page(abstract, rows)
    set_download_target_name(abstract, document)
    record_recording_date(abstract, rows)
    record_document_type(abstract, rows)
    record_grantor(abstract, rows)
    record_grantee(abstract, rows)
    record_related_documents(abstract, rows)
    record_legal(abstract, rows)
    record_empty_values(abstract, ['effective date', 'volume', 'document link'])
    record_comments(abstract, document)


# Write a function to check additional information for rows 4, 7
def record(browser, abstract, document):
    # document_table = access_document_table_data(browser, abstract, document)
    rows = get_document_content(browser, abstract, document)
    aggregate_document_information(abstract, rows, document)
