from engines.manta_ray.collect import collect
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id
from settings.general_functions import javascript_script_execution

# Similar functionality in "dolphin", "manta_ray", "octopus" & "swordfish" except for import


def search_results_page_loaded(browser, document):
    # page_header = locate_element_by_tag_name(browser, "h2", "page header", False, document)
    # if page_header.text.startswith("Search Results"):
    if browser.title.startswith("Search Results"):
        return True


def open_search_result(browser, abstract, document) -> bool:
    """
    Open the search result.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (dict): The abstract information.
        document (dict): The document information.

    Returns:
        bool: True if the search result is opened successfully, False otherwise.
    """
    if not document.description_link or document.result_number > 0:
        if not collect(browser, abstract, document):
            return False
    if abstract.program != "register_page_count":
        javascript_script_execution(browser, document.description_link)
        try:
            click_button(browser, locate_element_by_id, abstract.county.buttons["View Button"], "view document button", document, quick=True)
        except Exception:
            try:
                click_button(browser, locate_element_by_id, abstract.county.buttons["Purchase Button"], "purchase document button", document, quick=True)
            except Exception:
                pass
        return True
    return False

def open_document(browser, abstract, document):
    if search_results_page_loaded(browser, document):
        return open_search_result(browser, abstract, document)
