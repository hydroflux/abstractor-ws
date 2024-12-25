import subprocess
import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from webdriver_manager.core.os_manager import ChromeType

def delete_existing_chromedriver():
    chromedriver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
    chromedriver_dir = os.path.dirname(chromedriver_path)
    if os.path.exists(chromedriver_dir):
        print(f"Deleting existing ChromeDriver at {chromedriver_dir}")
        subprocess.run(["rm", "-rf", chromedriver_dir], check=True)
        print("Deleted existing ChromeDriver.")

# Look into how to change driver preferences mid script -- for download directories
def chrome_webdriver(abstract, retries=3, delay=5):
    print("Starting ChromeDriver setup...")
    delete_existing_chromedriver()
    chromedriver = ChromeDriverManager().install()
    print(f"ChromeDriver installed at: {chromedriver}")
    service = Service(chromedriver)
    options = webdriver.ChromeOptions()

    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Bypass OS Security Model
    options.add_argument('--no-sandbox')
    # Added for printing to PDF
    options.add_argument('--kiosk-printing')

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

    # Needs to be reviewed, but possibly can be used for adblock???
    # options.add_extension(‘Users/Desktop/Python Scripting/crx_files/adblock_plus_3_8_4_0.crx’)
    
    prefs = {
        # Setting Default Directory Doesn't work when using JSON.dumps
        'savefile.default_directory': f'{abstract.target_directory}/Documents',
        "download.default_directory": f'{abstract.target_directory}/Documents',
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        # Added for printing to PDF
        "printing.print_preview_sticky_settings.appState": json.dumps(settings)
    }

    # Add the preferences to the options
    options.add_experimental_option("prefs", prefs)
    # Turn-off userAutomationExtension
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

def enable_download_in_headless_chrome(browser, abstract):
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


def create_webdriver(abstract):
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
