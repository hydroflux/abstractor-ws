from engines.swordfish.collect import collect
from selenium_utilities.locators import locate_element_by_tag_name
from settings.general_functions import javascript_script_execution

# Similar functionality in "dolphin", "manta_ray", "octopus" & "swordfish" except for import


def search_results_page_loaded(browser, document):
    page_header = locate_element_by_tag_name(browser, "h2", "page header", False, document)
    if page_header.text.startswith("Results"):
        return True


def open_search_result(browser, abstract, document):
    if not document.description_link or document.result_number > 0:
        if not collect(browser, abstract, document):
            return False
    if abstract.program != "register_page_count":
        javascript_script_execution(browser, document.description_link)
        return True
    

def open_document(browser, abstract, document):
    if search_results_page_loaded(browser, document):
        return open_search_result(browser, abstract, document)

