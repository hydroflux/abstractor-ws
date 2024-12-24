"""
This module provides functions to handle the process of opening documents for the Komodo engine.
It includes functions to open the next result and open a specific document.

Functions:
    - next_result(browser: WebDriver, abstract: Any, document: Any) -> bool:
        -- Processes the next result and opens the corresponding document.
    - open_document(browser: WebDriver, abstract: Any, document: Any) -> bool:
        -- Opens a specific document based on the program type.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as opening URLs and handling different program types.

Imports:
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Local:
        - from selenium_utilities.open: For opening URLs.
    - Standard Library:
        - from typing: For type hints.

Usage:
    These functions are designed to be used with Selenium WebDriver to automate the process of opening documents for the Komodo engine.
    They provide robust handling of common issues such as navigating to URLs and ensuring the correct page is loaded,
    making it easier to write reliable web automation scripts.
"""

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Local Import(s)
from selenium_utilities.open import open_url

# Standard Library Import(s)
from typing import Any

def next_result(browser: WebDriver, abstract: Any, document: Any) -> bool:
    """
    Processes the next result and opens the corresponding document.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing program type and other information.
        document (Any): The document object containing result information.

    Returns:
        bool: True if the document was opened successfully, False otherwise.
    """
    print(f"Processing result number {document.result_number + 1} of {document.number_results}...")
    return open_document(browser, abstract, document)


def open_document(browser: WebDriver, abstract: Any, document: Any) -> bool:
    """
    Opens a specific document based on the program type.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing program type and other information.
        document (Any): The document object containing document-specific information.

    Returns:
        bool: True if the document was opened successfully, False otherwise.
    """
    if abstract.program == "name_search":
        open_url(browser, document.description_link, abstract.county.titles["Search Result Page"],
                 f"reception number {document.reception_number} at {document.description_link}")
        return True
    elif abstract.program in ["execute", "review"]:
        open_url(browser, document.result_links[document.result_number], abstract.county.titles["Search Result Page"],
                 f"reception number {document.reception_number} at {document.description_link}")
        return True
    else:
        input(f"""No open document function for a "{abstract.program}" program type, """
              f"""please review and enter to continue...""")
        return False