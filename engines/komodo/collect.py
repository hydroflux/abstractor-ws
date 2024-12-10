from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
import re
from selenium.webdriver.remote.webelement import WebElement

from classes.Abstract import Abstract
from classes.Document import Document
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name, locate_elements_by_css_selector, locate_element_by_css_selector, locate_element_by_tag_name


def count_total_search_results(browser: WebDriver, abstract: Abstract) -> Optional[int]:
    """
    Count the total number of search results.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.

    Returns:
        Optional[int]: The total number of search results, or None if not found.
    """
    try:
        # Locate the element containing the search result totals
        results_summary_element = locate_element_by_css_selector(browser, abstract.county.tags["Total Results"], "results summary")
        if results_summary_element:
            # Extract the number from the text using a regular expression
            results_text = results_summary_element.text
            match = re.search(r'of\s+([\d,]+)\s+results', results_text)
            if match:
                total_results = int(match.group(1).replace(',', ''))
                abstract.number_search_results = total_results
                print(f'Collection search returned "{total_results}" results for processing.')
                return total_results
    except Exception as e:
        print(f"Error getting total search results: {e}")
    return None


def get_total_pages(browser: WebDriver, abstract: Abstract) -> Optional[int]:
    """
    Get the total number of pages from the pagination.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.

    Returns:
        Optional[int]: The total number of pages, or None if not found.
    """
    try:
        # Locate the pagination buttons
        pagination_buttons = locate_elements_by_css_selector(browser, abstract.county.tags["Pagination"], "pagination buttons")
        if pagination_buttons:
            # Extract the page numbers and find the maximum value
            page_numbers = [int(button.get_attribute("value")) for button in pagination_buttons if button.get_attribute("value").isdigit()]
            if page_numbers:
                total_pages = max(page_numbers)
                print(f'Total number of pages: {total_pages}')
                return total_pages
    except Exception as e:
        print(f"Error getting total number of pages: {e}")
    return None


def get_results_table(browser: WebDriver, abstract: Abstract) -> Optional[WebElement]:
    """
    Get the search results table.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.

    Returns:
        Optional[WebElement]: The search results table element, or None if not found.
    """
    search_results = locate_element_by_class_name(browser, abstract.county.classes["Search Results"], "search results")
    if search_results:
        return locate_element_by_tag_name(search_results, abstract.county.tags["Search Results Table"], "search results table")
    return None


def access_result_reception_number(abstract: Abstract, result: WebElement) -> Optional[str]:
    """
    Access the reception number from the result row.

    Args:
        abstract (Abstract): The abstract information.
        result (WebElement): The result row element.

    Returns:
        Optional[str]: The reception number, or None if not found.
    """
    try:
        reception_number_element = locate_element_by_css_selector(result, abstract.county.tags["Reception Number Column"], "reception number")
        if reception_number_element:
            return reception_number_element.text
    except Exception as e:
        print(f"Error accessing reception number: {e}")
    return None


def access_result_description_link(abstract: Abstract, result: WebElement) -> Optional[str]:
    """
    Access the description link from the result row.

    Args:
        abstract (Abstract): The abstract information.
        result (WebElement): The result row element.

    Returns:
        Optional[str]: The description link, or None if not found.
    """
    try:
        # Extract the unique identifier from the checkbox input element's id attribute
        checkbox_element = locate_element_by_css_selector(result, abstract.county.tags["Result Checkbox"], "result checkbox")
        if checkbox_element:
            checkbox_id = checkbox_element.get_attribute("id")
            match = re.search(r'table-checkbox-(\d+)', checkbox_id)
            if match:
                unique_id = match.group(1)
                # Construct the URL using the extracted unique identifier
                description_link = f"{abstract.county.urls['Search Result Base Url']}{unique_id}"
                return description_link
    except Exception as e:
        print(f"Error accessing description link: {e}")
    return None


def build_document(abstract: Abstract, result: WebElement) -> Document:
    """
    Build a Document instance using the reception number and description link.

    Args:
        abstract (Abstract): The abstract information.
        result (WebElement): The result row element.

    Returns:
        Document: The built Document instance.
    """
    reception_number = access_result_reception_number(abstract, result)
    description_link = access_result_description_link(abstract, result)
    return Document(
        type="document_number",
        value=reception_number,
        reception_number=reception_number,
        description_link=description_link,
        county=abstract.county,
        number_results=1
    )


def process_search_result(abstract: Abstract, result: WebElement) -> None:
    """
    Process a single search result.

    Args:
        abstract (Abstract): The abstract information.
        result (WebElement): The result row element.
    """
    reception_number = access_result_reception_number(result)
    if reception_number:
        document = build_document(abstract, result)
        document.print_attributes()
        # Add the document to the document_list array on the abstract object instance
        abstract.document_list.append(document)


def process_search_results(browser: WebDriver, abstract: Abstract) -> None:
    """
    Process all search results in the table.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    search_results_table = get_results_table(browser, abstract)
    if search_results_table:
        # Process the search results on the current page
        results = locate_elements_by_css_selector(search_results_table, "tr", "search result rows")
        for result in results:
            # Process each search result
            process_search_result(abstract, result)


def process_search_result_pages(browser: WebDriver, abstract: Abstract) -> None:
    """
    Process search results across multiple pages.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    total_pages = get_total_pages(browser, abstract)
    for page in range(1, total_pages + 1):
        # Process each page of search results
        print(f"Processing page {page} of {total_pages}...")
        # Check if the current page is the last page
        if page < total_pages:
            click_button(browser, locate_element_by_css_selector, abstract.county.tags["Next Page"], "next page button")
        else:
            print("Reached the last page of search results.")
            if len(abstract.document_list) == abstract.number_search_results:
                print(f"Located {len(abstract.document_list)} of {abstract.number_search_results} search results.")
            else:
                input(f"Expected {abstract.number_search_results} search results, but located {len(abstract.document_list)}.")


def collect(browser: WebDriver, abstract: Abstract) -> None:
    """
    Collect search results from all pages.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    count_total_search_results(browser, abstract)
    if abstract.number_search_results > 50:
        process_search_result_pages(browser, abstract)
    else:
        search_results_table = get_results_table(browser, abstract)
        if search_results_table:
            process_search_results(abstract, search_results_table)
    print("Search results collected.")
