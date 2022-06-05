from classes.Document import Document

from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_elements_by_class_name)


def register_result_count(browser, abstract, document):
    result_count_container = locate_elements_by_class_name(browser, abstract.county.classes["Result Count Container"],
                                                           "result count container", False)[1]
    result_count_text = result_count_container.text.split("\n")[1]
    if document is None:
        abstract.number_search_results = int(result_count_text.split(" ")[-2])
    else:
        document.number_results = int(result_count_text.split(" ")[-2])


def count_results(browser, abstract, document):
    if not abstract.number_search_results:
        register_result_count(browser, abstract, document)


def access_result_rows(browser, abstract, document=None):
    return locate_elements_by_class_name(browser, abstract.county.classes["Result Row"], "result rows", False, document)


def access_result_reception_number(result):
    reception_number_field = result.text.split("\n")[1]
    return reception_number_field.split(" ")[0][1:]


def access_result_button(abstract, result, document=None):
    result_button = locate_element_by_class_name(result, abstract.county.buttons["Open Document"],
                                                 "result button", True, document)
    return result_button.get_attribute("href")


def build_document(abstract, result):
    reception_number = access_result_reception_number(result)
    description_link = access_result_button(abstract, result)
    return Document("document_number", reception_number, county=abstract.county, description_link=description_link)


def build_document_list(browser, abstract):
    result_rows = access_result_rows(browser, abstract)
    for row in result_rows:
        document = build_document(abstract, row)
        abstract.document_list.append(document)


def collect(browser, abstract, document=None):
    count_results(browser, abstract, document)
    if document is None:
        build_document_list(browser, abstract)
    else:
        result_rows = access_result_rows(browser, abstract, document)
        result = result_rows[document.result_number]
        document.description_link = access_result_button(abstract, result, document)
