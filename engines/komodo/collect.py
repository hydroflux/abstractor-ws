"""
Module to collect search results from a web page using Selenium.

This module contains functions to:
- Count the total number of search results.
- Access search result details such as reception number and description link.
- Build Document instances from search results.
- Process search results across multiple pages.
- Store the collected search results in the Abstract instance.
- Verify the final search results by comparing the expected and actual number of results.
- Set the "Results Per Page" to the highest available option.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as clicking buttons and locating elements by various selectors.

Imports:
    - Standard Library:
        - from typing: For type hints.
        - import math: For mathematical functions.
        - import re: For regular expressions.
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
        - from selenium.webdriver.remote.webelement: For WebElement interactions.
    - Local:
        - from selenium_utilities.inputs: For clicking buttons using Selenium.
        - from selenium_utilities.locators: For locating elements using various selectors.
    - Class:
        - from classes.Abstract: For Abstract class to store collected data.
        - from classes.Document: For Document class to store document information.
"""

# Standard Library Import(s)
from typing import Optional
import math
import re

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# Local Import(s)
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import (
    locate_element_by_class_name,
    locate_elements_by_class_name,
    locate_elements_by_css_selector,
    locate_element_by_css_selector,
    locate_element_by_tag_name
)

# Class Import(s)
from classes.Abstract import Abstract
from classes.Document import Document


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
        results_summary_element = locate_element_by_css_selector(browser, abstract.county.tags["Total Results"], "results summary")
        if results_summary_element:
            results_text = results_summary_element.text
            match = re.search(r'of\s+([\d,]+)\s+results', results_text)
            if match:
                total_results = int(match.group(1).replace(',', ''))
                if abstract.number_search_results is None:
                    abstract.number_search_results = total_results
                else:
                    abstract.number_search_results += total_results
                if total_results > 2:
                    print(f'Search returned "{str(total_results)}" results for processing.')
                return total_results
    except Exception as e:
        input(f"Error getting total search results: {e}")
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
        else:
            print("Reception number element not found to access result reception number.")
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
        checkbox_element = locate_element_by_css_selector(result, abstract.county.tags["Result Checkbox"], "result checkbox")
        if checkbox_element:
            checkbox_id = checkbox_element.get_attribute("id")
            match = re.search(r'table-checkbox-(\d+)', checkbox_id)
            if match:
                unique_id = match.group(1)
                description_link = f"{abstract.county.urls['Search Result Base Url']}{unique_id}"
                return description_link
        else:
            print("Checkbox element not found to access result description link.")
    except Exception as e:
        print(f"Error accessing description link: {e}")
    return None


def build_document(abstract: Abstract, reception_number: str, description_link: str) -> Document:
    """
    Build a Document instance using the reception number and description link.

    Args:
        abstract (Abstract): The abstract information.
        reception_number (str): The reception number.
        description_link (str): The description link.

    Returns:
        Document: The built Document instance.
    """
    return Document(
        type="document_number",
        value=reception_number,
        reception_number=reception_number,
        description_link=description_link,
        county=abstract.county,
        number_results=1
    )


def process_search_result(result: WebElement, abstract: Abstract, document: Optional[Document] = None) -> None:
    """
    Process a single search result.

    Args:
        result (WebElement): The result row element.
        abstract (Abstract): The abstract information.
        document (Optional[Document]): The document object, if applicable.
    """
    reception_number = access_result_reception_number(result, abstract)
    if reception_number:
        description_link = access_result_description_link(result, abstract)
        if abstract.program == "name_search":
            document = build_document(abstract, reception_number, description_link)
            abstract.document_list.append(document)
            print(f"Added document {len(abstract.document_list)} of {abstract.number_search_results} "
                  f"with reception number {reception_number} to the document list.")
        elif abstract.program in ["execute", "review"]:
            if reception_number == document.value:
                document.reception_number = reception_number
                document.result_links.append(description_link)
            else:
                input(f"Reception number '{reception_number}' does not match document value '{document.value}' number. Please review and press enter to continue.")
        else:
            input(f"No processing function for program type '{abstract.program}'. Please review and press enter to continue.")
    else:
        input("Unable to locate reception number for search result. Please review and press enter to continue.")


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


def process_search_results(browser: WebDriver, abstract: Abstract, document: Optional[Document] = None) -> None:
    """
    Process all search results in the table.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Optional[Document]): The document object, if applicable.
    """
    search_results_table = get_results_table(browser, abstract)
    if search_results_table:
        results = locate_elements_by_css_selector(search_results_table, "tr", "search result rows")
        for result in results:
            process_search_result(result, abstract, document)
    else:
        input("No search results table found.")


def process_search_result_pages(browser: WebDriver, abstract: Abstract) -> None:
    """
    Process search results across multiple pages.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
    """
    total_pages = math.ceil(abstract.number_search_results / 250)
    for page in range(1, total_pages + 1):
        print(f"Processing page {page} of {total_pages}...")
        process_search_results(browser, abstract)
        if page < total_pages:
            click_button(browser, locate_element_by_css_selector, abstract.county.tags["Next Page"], "next page button")
        else:
            print("Reached the last page of search results.")
            verify_final_search_results(abstract)


def collect(browser: WebDriver, abstract: Abstract, document: Optional[Document] = None) -> None:
    """
    Collect search results from all pages.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Optional[Document]): The document object, if applicable.
    """
    if abstract.program == "name_search" and abstract.number_search_results is None:
        total_results = count_total_search_results(browser, abstract)
        if abstract.number_search_results > 50:
            set_results_per_page_to_highest(browser, abstract)
            process_search_result_pages(browser, abstract)
        else:
            process_search_results(browser, abstract)
            verify_final_search_results(abstract)
    elif abstract.program in ["execute", "review"]:
        total_results = count_total_search_results(browser, abstract)
        document.number_results = total_results
        process_search_results(browser, abstract, document)