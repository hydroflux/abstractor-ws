from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_tag_name,
                                         locate_elements_by_class_name,
                                         locate_elements_by_tag_name)

from settings.general_functions import get_element_text, scroll_into_view

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open_document", __name__)


# def check_for_alert(browser, document):
#     print("Checking for browser alert related to search...")
#     if handle_alert(browser):
#         print("Alert located & handled, performing search execution again.")
#         search(browser, document)
#         return locate_result_count(browser, document)


# def locate_result_count(browser, document):
#     try:
#         result_count_present = EC.presence_of_element_located((By.ID, results_count_id))
#         WebDriverWait(browser, timeout).until(result_count_present)
#         result_count = browser.find_element_by_id(results_count_id)
#         return result_count
#     except TimeoutException:
#         print(f'Browser timed out trying to locate the number of results returned for '
#               f'{document.extrapolate_value()}.')
#         check_for_alert(browser)


def count_results(browser, abstract, document):
    result_count = locate_element_by_id(browser, abstract.county.ids["Results Count"],
                                        "results count", False, document)
    # 'check_For_alert' function originally followed the timeout exception in 'locate_result_count' function
    #  If result count == none, perform a "re-search"
    return result_count.text.split(' ')[-1]


def get_results_table_body(browser, abstract, document):
    results_table = locate_element_by_id(browser, abstract.county.ids["Results Table"],
                                         "results table", False, document)
    scroll_into_view(browser, results_table)
    return locate_element_by_tag_name(results_table, abstract.county.tags["Results Table Body"],
                                      "results table body", False, document)


def get_result_rows(browser, abstract, document):
    results_table_body = get_results_table_body(browser, abstract, document)
    return locate_elements_by_class_name(results_table_body, abstract.county.classes["Result Rows"],
                                         "result rows", False, document)


def verify_document_number(document, cells):
    if document.document_value() in map(get_element_text, cells):
        return True


def verify_book_and_page_numbers(document, cells):
    book, page = document.document_value()
    if book and page in map(get_element_text, cells):
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


def count_matching_results(browser, abstract, document):
    result_rows = get_result_rows(browser, abstract, document)
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
    count_results(browser, abstract, document)
    return verify_results(browser, abstract, document)
