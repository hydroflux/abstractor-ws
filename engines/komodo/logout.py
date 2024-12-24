"""
This module provides functions to handle the logout process for the Komodo engine.
It includes a function to log out of the application.

Functions:
    - logout(browser: WebDriver, abstract: Any) -> None:
        -- Logs out of the application by navigating to the logout page.

Imports:
    - Local:
        - from selenium_utilities.open: For opening URLs.
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Class:
        - from classes.Abstract: For Abstract class to store collected data.

Usage:
    This function is designed to be used with Selenium WebDriver to automate the logout process for the Komodo engine.
    It navigates to the logout page to log out of the application.
"""

# Local Import(s)
from selenium_utilities.open import open_url

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Class Import(s)
from classes import Abstract


def logout(browser: WebDriver, abstract: Abstract) -> None:
    """
    Logs out of the application by navigating to the logout page.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Any): The abstract object containing county-specific information.
    """
    open_url(
        browser,
        abstract.county.urls["Logout Page"],
        abstract.county.titles["Logout Page"],
        "logout page"
    )