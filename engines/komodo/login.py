"""
This module provides functions to handle the login process for the Komodo engine.
It includes functions to enter user credentials and perform the login action.

Functions:
    - enter_credentials(browser: WebDriver, abstract: Any) -> None:
        -- Enters the user credentials into the login form.
    - login(browser: WebDriver, abstract: Any) -> None:
        -- Opens the login page and enters the user credentials to perform the login action.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as locating elements, clicking buttons, and entering values.

Imports:
    - Selenium:
        - from selenium.webdriver.remote.webdriver: For WebDriver interactions.
    - Local:
        - from selenium_utilities.inputs: For clicking buttons and entering input values.
        - from selenium_utilities.locators: For locating elements.
        - from selenium_utilities.open: For opening URLs.
    - Class:
        - from classes.Abstract: For Abstract class to store collected data.

Usage:
    These functions are designed to be used with Selenium WebDriver to automate the login process for the Komodo engine.
    They provide robust handling of common issues such as waiting for elements to load and ensuring elements are clickable,
    making it easier to write reliable web automation scripts.
"""

# Selenium Import(s)
from selenium.webdriver.remote.webdriver import WebDriver

# Local Import(s)
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_id
from selenium_utilities.open import open_url

# Class Import(s)
from classes.Abstract import Abstract


def enter_credentials(browser: WebDriver, abstract: Abstract) -> None:
    """
    Enters the user credentials into the login form.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing user credentials and other information.
    """
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[0],
                      "username input", abstract.county.credentials[1])
    enter_input_value(browser, locate_element_by_id, abstract.county.credentials[2],
                      "password input", abstract.county.credentials[3])
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Login"], "login button")


def login(browser: WebDriver, abstract: Abstract) -> None:
    """
    Opens the login page and enters the user credentials to perform the login action.

    Args:
        browser (WebDriver): The WebDriver instance used to interact with the browser.
        abstract (Abstract): The abstract object containing user credentials and other information.
    """
    open_url(browser, abstract.county.urls["Login Page"],
             abstract.county.titles["Login Page"], "county site")
    enter_credentials(browser, abstract)