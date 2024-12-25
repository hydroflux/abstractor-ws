"""
This module provides functionality for setting up and managing a Chrome WebDriver instance.
It includes functions to delete existing ChromeDriver installations, configure Chrome options,
and create a WebDriver instance with specified preferences and settings.

Functions:
    - delete_existing_chromedriver() -> None:
        -- Deletes the existing ChromeDriver installation.
    - chrome_webdriver(abstract: Abstract, retries: int = 3, delay: int = 5) -> webdriver.Chrome:
        -- Sets up and returns a Chrome WebDriver instance with specified options and preferences.
    - enable_download_in_headless_chrome(browser: webdriver.Chrome, abstract: Abstract) -> None:
        -- Enables download functionality in headless Chrome mode.
    - create_webdriver(abstract: Abstract) -> webdriver.Chrome:
        -- Creates and returns a Chrome WebDriver instance, enabling download in headless mode if specified.

The functions in this module interact with web elements using Selenium WebDriver
and perform actions such as locating elements, clicking buttons, and entering values.

Imports:
    - Standard Library:
        - import json: For handling JSON data.
        - import os: For interacting with the operating system.
        - import subprocess: For running subprocesses.
        - from time import sleep: For adding delays between retries.
    - Selenium:
        - from selenium import webdriver: For WebDriver interactions.
        - from selenium.common.exceptions import WebDriverException: For handling WebDriver exceptions.
        - from selenium.webdriver.chrome.service import Service: For managing the ChromeDriver service.
    - WebDriver Manager:
        - from webdriver_manager.chrome import ChromeDriverManager: For managing ChromeDriver installations.
        - from webdriver_manager.core.os_manager import ChromeType: For specifying the type of ChromeDriver.
    - Class:
        - from classes.Abstract import Abstract: For Abstract class to store collected data.

Usage:
    These functions are designed to be used with Selenium WebDriver to automate the setup and management of ChromeDriver.
    They provide robust handling of common issues such as ensuring a fresh installation of ChromeDriver and configuring
    browser options, making it easier to write reliable web automation scripts.
"""

# Standard Library Import(s)
import json
import os
import subprocess
from time import sleep

# Selenium Import(s)
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service

# WebDriver Manager Import(s)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Class Import(s)
from classes.Abstract import Abstract


def delete_existing_chromedriver() -> None:
    """
    Deletes the existing ChromeDriver installation.

    This function locates the current ChromeDriver installation directory and deletes it
    to ensure a fresh installation of ChromeDriver.
    """
    chromedriver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
    chromedriver_dir = os.path.dirname(chromedriver_path)
    if os.path.exists(chromedriver_dir):
        print(f"Deleting existing ChromeDriver at {chromedriver_dir}")
        subprocess.run(["rm", "-rf", chromedriver_dir], check=True)
        print("Deleted existing ChromeDriver.")


def chrome_webdriver(abstract: Abstract, retries: int = 3, delay: int = 5) -> webdriver.Chrome:
    """
    Sets up and returns a Chrome WebDriver instance with specified options and preferences.

    Args:
        abstract (Abstract): The abstract object containing configuration details.
        retries (int, optional): The number of retry attempts if ChromeDriver fails to start. Defaults to 3.
        delay (int, optional): The delay between retry attempts in seconds. Defaults to 5.

    Returns:
        webdriver.Chrome: The configured Chrome WebDriver instance.
    """
    print("Starting ChromeDriver setup...")
    delete_existing_chromedriver()
    chromedriver = ChromeDriverManager().install()
    print(f"ChromeDriver installed at: {chromedriver}")
    service = Service(chromedriver)
    options = webdriver.ChromeOptions()

    # Disable the AutomationControlled flag to avoid detection by websites
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Bypass OS security model (useful in Docker containers)
    options.add_argument('--no-sandbox')
    # Enable kiosk printing mode (useful for printing to PDF)
    options.add_argument('--kiosk-printing')
    # Disable GPU hardware acceleration (useful in headless mode)
    options.add_argument('--disable-gpu')
    # Set the default window size
    options.add_argument('window-size=1920x1080')
    # Disable browser extensions
    options.add_argument('--disable-extensions')
    # Disable /dev/shm usage (useful in Docker containers)
    options.add_argument('--disable-dev-shm-usage')
    # Enable logging for debugging
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    

    # Set headless mode if enabled
    if abstract.headless:
        options.add_argument('--headless')
        print("Running in headless mode.")
        # options.add_argument('start-maximized') # Maximize Viewport


    # Settings used for printing directly to PDF
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    
    prefs = {
        # Set the default directory for saving files
        'savefile.default_directory': f'{abstract.target_directory}/Documents',
        # Set the default directory for downloads
        "download.default_directory": f'{abstract.target_directory}/Documents',
        # Disable the download prompt
        "download.prompt_for_download": False,
        # Ensure PDFs are opened externally
        "plugins.always_open_pdf_externally": True,
        # Set the print preview settings for saving as PDF
        "printing.print_preview_sticky_settings.appState": json.dumps(settings),
        # Disable password manager
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # Disable browser notifications
        "profile.default_content_setting_values.notifications": 2,
        # Allow automatic downloads
        "profile.default_content_setting_values.automatic_downloads": 1
    }

    # Add the preferences to the options
    options.add_experimental_option("prefs", prefs)
    # Turn off the automation extension
    options.add_experimental_option("useAutomationExtension", False)
    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    print("Chrome options set. Attempting to start ChromeDriver...")
    attempt = 0
    while attempt < retries:
        try:
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            print("ChromeDriver started successfully.")
            return driver
        except WebDriverException as e:
            print(f"Failed to start ChromeDriver service: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying to start ChromeDriver service... (Attempt {attempt + 1} of {retries})")
                sleep(delay)
            else:
                print("Exceeded maximum retries. Raising exception.")
                raise


def enable_download_in_headless_chrome(browser: webdriver.Chrome, abstract: Abstract) -> None:
    """
    Enables download functionality in headless Chrome mode.

    Args:
        browser (webdriver.Chrome): The Chrome WebDriver instance.
        abstract (Abstract): The abstract object containing configuration details.
    """
    document_directory = f'{abstract.target_directory}/Documents'
    print(f"""Enabling download in headless Chrome. Download directory: "{document_directory}" """)

    browser.command_executor._commands["send_command"] = (
        "POST",
        '/session/$sessionId/chromium/send_command'
    )

    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': document_directory
        }
    }
    browser.execute("send_command", params)
    print("Download behavior set in headless Chrome.")


def create_webdriver(abstract: Abstract) -> webdriver.Chrome:
    """
    Creates and returns a Chrome WebDriver instance, enabling download in headless mode if specified.

    Args:
        abstract (Abstract): The abstract object containing configuration details.

    Returns:
        webdriver.Chrome: The configured Chrome WebDriver instance.
    """
    try:
        print("Creating WebDriver...")
        browser = chrome_webdriver(abstract)
        if abstract.headless:
            enable_download_in_headless_chrome(browser, abstract)
        print("WebDriver created successfully.")
        return browser
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting...")
        exit(0)
