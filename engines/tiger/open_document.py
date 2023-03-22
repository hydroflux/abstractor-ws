# from project_management.timers import naptime
from selenium_utilities.element_interaction import get_element_text
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_tag_name, locate_elements_by_class_name,
                                         locate_elements_by_tag_name)
from settings.general_functions import scroll_into_view


def count_results(browser, abstract, document):
    click_button(browser, locate_element_by_id, abstract.county.buttons["Result Count"],
                 "result count button", document)  # Open Result Count
    result_count = None
    while result_count is None or result_count.text == abstract.county.messages["Counting"]:
        result_count = locate_element_by_id(browser, abstract.county.ids["Result Count"],
                                            "result count", document=document)  # Get Result Count
        # result_count = locate_element_by_id(browser, abstract.county.ids["Results Count"],
        #                                     "results count", False, document)
    return int(result_count.text.split(' ')[-1])


# def count_results(browser, abstract, document):
    # click_button(browser, locate_element_by_id, abstract.county.buttons["Result Count"],
    #              "result count button", document)  # Open Result Count
#     naptime()
#     naptime()
#     result_count = locate_element_by_id(browser, abstract.county.ids["Result Count"],
#                                         "result count", document=document)  # Get Result Count
#     # This doesn't work the way it's supposed to
#     # Need to perform a match against the document number in order to find the correct count
#     # Check leopard for options
#     if int(result_count.text.split(' ')[-1]) > 1:
#         document.number_results = 1


def get_results_table_body(browser, abstract, document):
    results_table = locate_element_by_id(browser, abstract.county.ids["Results Table"],
                                         "results table", False, document)
    scroll_into_view(browser, results_table)
    return locate_element_by_tag_name(results_table, abstract.county.tags["Results Table Body"],
                                      "results table body", False, document)


# def access_results_table(browser, abstract, document):
#     results = locate_element_by_id(browser, abstract.county.ids["Results Table"],
#                                    "results section", document=document)
#     results_table = locate_element_by_tag_name(results, abstract.county.tags["Body"],
#                                                "results table", document=document)
#     return results_table


def get_result_rows(browser, abstract, document):
    results_table_body = get_results_table_body(browser, abstract, document)
    return locate_elements_by_class_name(results_table_body, abstract.county.classes["Result Rows"],
                                         "result rows", False, document)


# def access_first_row(abstract, document, results_table):
#     all_results = locate_elements_by_tag_name(results_table, abstract.county.tags["Rows"],
#                                               "search results", document=document)
#     return all_results[0]


def verify_document_number(document, cells):
    if document.document_value() in map(get_element_text, cells):
        return True


def verify_book_and_page_numbers(document, cells):
    book, page = document.document_value()
    book = book.zfill(4)
    page = page.zfill(4)
    if book and page in map(get_element_text, cells):
        return True
    elif book and f'{page[1:]}A' in map(get_element_text, cells):
        return True
    elif book and f'{page[1:]}B' in map(get_element_text, cells):
        return True
    elif book and f'{page[1:]}C' in map(get_element_text, cells):
        return True


def verify_result(document, cells):
    if document.type == "document_number":
        return verify_document_number(document, cells)
    elif document.type == "book_and_page":
        return verify_book_and_page_numbers(document, cells)


def check_result(browser, abstract, document, row):
    row_cells = locate_elements_by_tag_name(row, abstract.county.tags["Result Cell"],
                                            "result row cells", False, document)
    if verify_result(document, row_cells):
        document.number_results += 1
        return True


# def check_result(browser, abstract, document, results_table):
#     first_result = access_first_row(abstract, document, results_table)
#     center_element(browser, first_result)
#     first_result_cells = first_result.find_elements_by_tag_name(abstract.county.tags["Data"])
#     if document.value in map(get_element_text, first_result_cells):
#         return True


def count_matching_results(browser, abstract, document):
    result_rows = get_result_rows(browser, abstract, document)
    # remove next line after figuring the issue with count results
    if result_rows is not None:
        for row in result_rows:
            if not check_result(browser, abstract, document, row):
                break


def get_first_row(browser, abstract, document):
    result_rows = get_result_rows(browser, abstract, document)
    return result_rows[0]


def verify_results(browser, abstract, document):
    count_matching_results(browser, abstract, document)
    if document.number_results > 0:
        get_first_row(browser, abstract, document).click()
        return True


def open_document(browser, abstract, document):
    if count_results(browser, abstract, document) > 0:
        return verify_results(browser, abstract, document)


# def open_document(browser, abstract, document):
#     count_results(browser, abstract, document)
#     results_table = access_results_table(browser, abstract, document)
#     if check_result(browser, abstract, document, results_table):
#         access_first_row(abstract, document, results_table).click()
#         return True
