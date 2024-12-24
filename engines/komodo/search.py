"""
This module provides functions to handle the search process for the Komodo engine.
It includes functions to perform name searches, document searches, and handle the overall search process.

Functions:
    - perform_name_search(browser: WebDriver, abstract: Any) -> None:
        -- Performs a name search by entering the search criteria and executing the search.
    - perform_document_search(browser: WebDriver, abstract: Any, document: Any) -> None:
        -- Performs a document search by entering the search criteria and executing the search.
    - handle_search(browser: WebDriver, abstract: Any, document: Any) -> bool:
        -- Determines the type of search to perform and executes it.
    - search(browser: WebDriver, abstract: Any, document: Any) -> None:
        -- Handles the search process and collects results if the search is successful.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as locating elements, clicking buttons, and entering values.

Imports:
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Local:
        - from engines.komodo.collect: For collecting search results.
        - from project_management.timers: For handling page wait times.
        - from selenium_utilities.inputs: For clicking buttons and entering input values.
        - from selenium_utilities.locators: For locating elements.
        - from selenium_utilities.open: For opening URLs.
    - Class:
        - from classes.Abstract: For Abstract class to store collected data.
        - from classes.Document: For Document class to represent individual documents.

Usage:
    These functions are designed to be used with Selenium WebDriver to automate the search process for the Komodo engine.
    They provide robust handling of common issues such as waiting for elements to load and ensuring elements are clickable,
    making it easier to write reliable web automation scripts.
"""

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Local Import(s)
from engines.komodo.collect import collect
from project_management.timers import wait_for_page
from selenium_utilities.inputs import click_button, enter_input_value, enter_datepicker_value
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_css_selector
from selenium_utilities.open import open_url

# Class Import(s)
from classes.Abstract import Abstract
from classes.Document import Document


def perform_name_search(browser: WebDriver, abstract: Abstract) -> None:
    """
    Performs a name search by entering the search criteria and executing the search.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing search criteria and other information.
    """
    enter_input_value(browser, locate_element_by_css_selector, abstract.county.inputs["Search Input"],
                      "search value input", abstract.search_name, document=None)
    enter_datepicker_value(browser, locate_element_by_css_selector, abstract.county.inputs["Start Date"],
                      "search start date input", abstract.start_date, document=None)
    enter_datepicker_value(browser, locate_element_by_css_selector, abstract.county.inputs["End Date"],
                      "search end date input", abstract.end_date, document=None)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document=None)


def perform_document_search(browser: WebDriver, abstract: Abstract, document: Document) -> None:
    """
    Performs a document search by entering the search criteria and executing the search.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing search criteria and other information.
        document (Document, optional): The document object containing document-specific information.
    """
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "search page")
    value = document.document_value()
    enter_input_value(browser, locate_element_by_css_selector, abstract.county.inputs["Search Input"],
                      "search value input", value, document)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document)


def handle_search(browser: WebDriver, abstract: Abstract, document: Document = None) -> bool:
    """
    Determines the type of search to perform and executes it.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing search criteria and other information.
        document (Document, optional): The document object containing document-specific information. Defaults to None.

    Returns:
        bool: True if the search was performed successfully, False otherwise.
    """
    if abstract.program == "name_search" and not abstract.number_search_results:
        perform_name_search(browser, abstract)
        return True
    else:
        perform_document_search(browser, abstract, document)
        return True


def search(browser: WebDriver, abstract: Abstract, document: Document = None) -> None:
    """
    Handles the search process and collects results if the search is successful.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing search criteria and other information.
        document (Document, optional): The document object containing document-specific information. Defaults to None.
    """
    while True:
        collect_results = handle_search(browser, abstract, document)
        if collect_results and wait_for_page(browser, abstract.county.titles["Loading"], abstract.county.titles["Search Results Page"]):
            collect(browser, abstract, document)
            break
        else:
            break