from project_management.timers import naptime
from selenium_utilities.element_interaction import (center_element,
                                                    get_element_text)
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_tag_name,
                                         locate_elements_by_tag_name)


def count_results(browser, abstract, document):
    # Wait for results table to load before getting count
    locate_element_by_id(browser, abstract.county.ids["Results Table"],
                         "results table", False, document)
    # I don't think the above is doing anything useful
    naptime()
    # Need to find a better trigger to wait on
    result_count = locate_element_by_id(browser, abstract.county.ids["Result Count"],
                                        "result count", False, document)
    # This doesn't work the way it's supposed to
    # Need to perform a match against the document number in order to find the correct count
    # Check leopard for options
    if int(result_count.text.split(' ')[-1]) > 1:
        if document.type == "document_search":
            document.number_results = 1
        elif document.type == "name":
            document.number_results = int(result_count.text.split(' ')[-1])


def access_results_table(browser, abstract, document):
    results = locate_element_by_id(browser, abstract.county.ids["Results Table"],
                                   "results table", False, document)
    center_element(browser, results)
    results_table = locate_element_by_tag_name(results, abstract.county.tags["Table Body"],
                                               "results table body", False, document)
    return results_table


def access_first_row(abstract, document, results_table):
    all_results = locate_elements_by_tag_name(results_table, abstract.county.tags["Rows"],
                                              "search results", document=document)
    return all_results[0]


def check_result(browser, abstract, document, results_table):
    first_result = access_first_row(abstract, document, results_table)
    center_element(browser, first_result)
    first_result_cells = first_result.find_elements_by_tag_name(abstract.county.tags["Data"])
    if document.value in map(get_element_text, first_result_cells):
        return True


def open_document(browser, abstract, document):
    count_results(browser, abstract, document)
    results_table = access_results_table(browser, abstract, document)
    if check_result(browser, abstract, document, results_table):
        access_first_row(abstract, document, results_table).click()
        return True
