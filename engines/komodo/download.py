"""
This module provides functions to handle the document download process for the Komodo engine.
It includes functions to create the document download value and execute the download process.

Functions:
    - create_document_download_value(browser: WebDriver, abstract: Abstract) -> Optional[str]:
        -- Creates the document download value by locating the document ID and order ID elements.
    - execute_download(browser: WebDriver, abstract: Abstract, document: Document) -> None:
        -- Executes the download process by clicking the necessary buttons and creating the download value.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as locating elements and clicking buttons.

Imports:
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Local:
        - from selenium_utilities.inputs: For clicking buttons using Selenium.
        - from selenium_utilities.locators: For locating elements using various selectors.
    - Standard Library:
        - from typing: For type hints.
    - Class:
        - from classes.Abstract: For Abstract class to store collected data.
        - from classes.Document: For Document class to store document data.
"""

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Local Import(s)
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_css_selector, locate_element_by_tag_name

# Standard Library Import(s)
from typing import Optional

# Class Import(s)
from classes.Abstract import Abstract
from classes.Document import Document


def create_document_download_value(browser: WebDriver, abstract: Abstract) -> Optional[str]:
    """
    Creates the document download value by locating the document ID and order ID elements.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing county-specific information.

    Returns:
        Optional[str]: The created document download value, or None if an error occurred.
    """
    try:
        # Locate the Document ID element
        image_section = locate_element_by_class_name(browser, abstract.county.classes["Document Image Section"], "svg element")
        image_element = locate_element_by_tag_name(image_section, abstract.county.tags["Document Image"], "svg element")
        image_url = image_element.get_attribute(abstract.county.tags["Document Image Attribute"])
        document_id = image_url.split('/')[-1].split('_')[0]

        # Locate the Order ID element
        order_id_element = locate_element_by_css_selector(browser, abstract.county.tags["Order ID"], "order ID element")
        order_id = order_id_element.text
        
        # Create the final string
        download_value_final_string = f"{order_id}_{document_id}{abstract.county.inputs['Stock Download Suffix']}"
        print(f"Created string: {download_value_final_string}")

        return download_value_final_string
    except Exception as e:
        print(f"An error occurred while creating the string: {e}")
        return None


def execute_download(browser: WebDriver, abstract: Abstract, document: Document) -> None:
    """
    Executes the download process by clicking the necessary buttons and creating the download value.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing county-specific information.
        document (Any): The document object to be downloaded.
    """
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Purchase Window"], "purchase window", document)
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Purchase"], "purchase button", document)
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Download"], "download button", document)
    document.download_value = create_document_download_value(browser, abstract)