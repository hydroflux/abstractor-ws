"""
This module provides functions to execute the main program for the Komodo engine.
It includes functions to check for a document list and execute the main program.

Functions:
    - check_for_document_list(browser: WebDriver, abstract: Any) -> None:
        -- Checks if the program type requires a document list and performs a search if necessary.
    - execute_program(browser: WebDriver, abstract: Any) -> None:
        -- Executes the main program by logging in, checking for a document list, searching documents, and closing the program.

Imports:
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Local:
        - from engines.komodo.download: For executing the download process.
        - from engines.komodo.login: For logging in.
        - from engines.komodo.logout: For logging out.
        - from engines.komodo.open_document: For opening documents and processing the next result.
        - from engines.komodo.record: For recording document information.
        - from engines.komodo.search: For performing searches.
        - from serializers.executor: For closing the program and searching documents from a list.
    - Class:
        - None

Usage:
    These functions are designed to be used with Selenium WebDriver to automate the main program execution for the Komodo engine.
    They provide robust handling of common issues such as logging in, searching, and downloading documents,
    making it easier to write reliable web automation scripts.
"""

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Local Import(s)
from engines.komodo.download import execute_download
from engines.komodo.login import login
from engines.komodo.logout import logout
from engines.komodo.open_document import next_result, open_document
from engines.komodo.record import record
from engines.komodo.search import search
from serializers.executor import close_program, search_documents_from_list

# Class Import(s)
from classes.Abstract import Abstract


# Same code functionality in "dolphin", "manta_ray", & "swordfish" (except for imports)
# This code snippet can be refactored into a common function to reduce duplication.

def check_for_document_list(browser: WebDriver, abstract: Abstract) -> None:
    """
    Checks if the program type requires a document list and performs a search if necessary.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing program type and other information.
    """
    if abstract.program in ['name_search', 'legal']:
        search(browser, abstract)


def execute_program(browser: WebDriver, abstract: Abstract) -> None:
    """
    Executes the main program by logging in, checking for a document list, searching documents, and closing the program.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing program type and other information.
    """
    login(browser, abstract)
    check_for_document_list(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download,
        next_result
    )
    close_program(browser, abstract, logout)