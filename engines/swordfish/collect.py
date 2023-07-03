from classes.Document import Document

from selenium_utilities.locators import (locate_element, locate_element_by_class_name,
                                         locate_elements_by_class_name)

# Similar to "octopus" & "dolphin"


def register_number_results(browser, abstract, document):
    number_results_container = locate_elements_by_class_name(browser, abstract.county.classes["Result Count Container"],
                                                             "result count container", False)[1]
    number_results_text = number_results_container.text.split("\n")[2]
    number_results = int(number_results_text.split(" ")[-2])
    if document is None:
        print(f'Collection search returned "{str(number_results)}" results for processing.')
        abstract.number_search_results = number_results
    else:
        document.number_results = number_results


def count_results(browser, abstract, document):
    # need to create a unified handler rather than calling the function twice
    if document is not None and document.number_results == 0:
        register_number_results(browser, abstract, document)
    elif not abstract.number_search_results:
        register_number_results(browser, abstract, document)


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
    return Document(
        "document_number",
        reception_number,
        county=abstract.county,
        description_link=description_link,
        number_results=1
    )


def build_document_list(browser, abstract):
    result_rows = access_result_rows(browser, abstract)
    for row in result_rows:
        document = build_document(abstract, row)
        abstract.document_list.append(document)


def report_page_count(document, page_count):
    if document.number_results == 1:
        print(f'Document located at {document.extrapolate_value()} is {page_count} page(s)')
    elif document.number_results > 1:
        print(f'Documents located at {document.extrapolate_value()} are a combined {page_count} page(s)')


def register_result_page_count(abstract, document, result_rows):
    for result in result_rows:
        # page count container also contains information about the date of the document--
        # could be useful for determining when to update recording dates
        page_count_container = locate_element(result, "class", "span1",
                                              "page count container", False, document=document)
        page_count_element = locate_element(page_count_container, "tags", "span",
                                            "page count element", False, document=document)[-1]
        page_count = page_count_element.text.split(" ")[0]
        abstract.total_page_count += int(page_count)
    report_page_count(document, page_count)


def collect(browser, abstract, document=None):
    count_results(browser, abstract, document)
    if document.number_results != 0 and abstract.number_search_results != 0:
        if document is None:
            # Consider adding function for counting # of pages for "legal" program searches
            build_document_list(browser, abstract)
        else:
            result_rows = access_result_rows(browser, abstract, document)
            if document.result_number == 0:
                register_result_page_count(abstract, document, result_rows)
            result = result_rows[document.result_number]
            document.description_link = access_result_button(abstract, result, document)
        return True
