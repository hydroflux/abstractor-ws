"""
Module to collect search results from a web page using Selenium.

This module contains functions to:
- Count the total number of search results.
- Get the total number of pages from the pagination.
- Access search result details such as reception number and description link.
- Build Document instances from search results.
- Process search results across multiple pages.
- Store the collected search results in the Abstract instance.
- Verify the final search results by comparing the expected and actual number of results.
- Set the "Results Per Page" to the highest available option.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as clicking buttons and locating elements by various selectors.
"""

# Library Import(s)
from typing import Optional  # Library to provide hints about the types used in the source code
import re  # Library to provide support for regular expressions

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver  # WebDriver instance for browser interactions
from selenium.webdriver.remote.webelement import WebElement  # WebElement instance for web element interactions

# Local Import(s)
from classes.Abstract import Abstract  # For Abstract class to store collected data
from classes.Document import Document  # For Document class to represent individual documents
from selenium_utilities.inputs import click_button  # For clicking buttons using Selenium
from selenium_utilities.locators import (  # For locating elements using various selectors
    locate_element_by_class_name,
    locate_elements_by_class_name,
    locate_elements_by_css_selector,
    locate_element_by_css_selector,
    locate_element_by_tag_name
)


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


def locate_results_per_page_dropdown(browser: WebDriver, abstract: Abstract) -> Optional[WebElement]:
    """
    Locate the "Results Per Page" dropdown container.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.

    Returns:
        Optional[WebElement]: The located dropdown container element, or None if not found.
    """
    dropdown_containers = locate_elements_by_class_name(browser, abstract.county.classes["Results Per Page Container"], "sort dropdown containers")
    for container in dropdown_containers:
        label_element = locate_element_by_class_name(container, abstract.county.classes["Results Per Page Label"], "sort dropdown label")
        if label_element and label_element.text == "Results Per Page:":
            return container
    return None


def click_highest_option(dropdown_container: WebElement, abstract: Abstract) -> None:
    """
    Click on the highest available option in the dropdown menu.

    Args:
        dropdown_container (WebElement): The located dropdown container element.
        abstract (Abstract): The abstract information.
    """
    options_container = locate_element_by_class_name(dropdown_container, abstract.county.classes["Results Per Page Dropdown"], "dropdown options container")
    if options_container:
        options = locate_elements_by_class_name(options_container, abstract.county.classes["Results Per Page Options"], "dropdown options", clickable=True)
        if options:
            highest_option = options[-1]  # Assuming the highest option is the last one in the list
            highest_option.click()


def set_results_per_page_to_highest(browser: WebDriver, abstract: Abstract) -> None:
    """
    Set the "Results Per Page" to the highest available option.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    dropdown_container = locate_results_per_page_dropdown(browser, abstract)
    if dropdown_container:
        click_button(dropdown_container, locate_element_by_class_name, abstract.county.classes["Results Per Page Button"], "dropdown button", quick=True)
        click_highest_option(dropdown_container, abstract)


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


def access_result_reception_number(result: WebElement, abstract: Abstract) -> Optional[str]:
    """
    Access the reception number from the result row.

    Args:
        result (WebElement): The result row element.
        abstract (Abstract): The abstract information.

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


def access_result_description_link(result: WebElement, abstract: Abstract) -> Optional[str]:
    """
    Access the description link from the result row.

    Args:
        result (WebElement): The result row element.
        abstract (Abstract): The abstract information.

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


def build_document(result: WebElement, abstract: Abstract) -> Document:
    """
    Build a Document instance using the reception number and description link.

    Args:
        result (WebElement): The result row element.
        abstract (Abstract): The abstract information.

    Returns:
        Document: The built Document instance.
    """
    reception_number = access_result_reception_number(result, abstract)
    description_link = access_result_description_link(result, abstract)
    return Document(
        type="document_number",
        value=reception_number,
        reception_number=reception_number,
        description_link=description_link,
        county=abstract.county,
        number_results=1
    )


def process_search_result(result: WebElement, abstract: Abstract) -> None:
    """
    Process a single search result.

    Args:
        result (WebElement): The result row element.
        abstract (Abstract): The abstract information.
    """
    reception_number = access_result_reception_number(result, abstract)
    if reception_number:
        document = build_document(result, abstract)
        # Add the document to the document_list array on the abstract object instance
        abstract.document_list.append(document)


def verify_final_search_results(abstract: Abstract) -> None:
    """
    Verify the final search results by comparing the expected and actual number of results.

    Args:
        abstract (Abstract): The abstract information containing the document list and expected number of search results.
    """
    actual_results = len(abstract.document_list)
    expected_results = abstract.number_search_results
    if actual_results == expected_results:
        print(f"Located {actual_results} of {expected_results} search results.")
    else:
        input(f"Expected {expected_results} search results, but located {actual_results}. Please review and press enter to continue.")


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
            process_search_result(result, abstract)
    else:
        print("No search results table found.")


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
        process_search_results(browser, abstract)
        # Check if the current page is the last page
        if page < total_pages:
            click_button(browser, locate_element_by_css_selector, abstract.county.tags["Next Page"], "next page button")
        else:
            print("Reached the last page of search results.")
            verify_final_search_results(abstract)


def collect(browser: WebDriver, abstract: Abstract) -> None:
    """
    Collect search results from all pages.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    count_total_search_results(browser, abstract)
    if abstract.number_search_results > 50:
        set_results_per_page_to_highest(browser, abstract)
        process_search_result_pages(browser, abstract)
    else:
        process_search_results(browser, abstract)
        verify_final_search_results(abstract)