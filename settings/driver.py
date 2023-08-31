import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# # helper to edit 'Preferences' file inside Chrome profile directory.
# def set_download_directory(profile_path, profile_name, download_path):
#     prefs_path = os.path.join(profile_path, profile_name, 'Preferences')
#     with open(prefs_path, 'r') as f:
#         prefs_dict = json.loads(f.read())
#     prefs_dict['download']['default_directory'] = download_path
#     prefs_dict['savefile']['directory_upgrade'] = True
#     prefs_dict['download']['directory_upgrade'] = True
#     with open(prefs_path, 'w') as f:
#         json.dump(prefs_dict, f)


# Look into how to change driver preferences mid script -- for download directories
def chrome_webdriver(abstract):
    chromedriver = ChromeDriverManager().install()
    service = Service(chromedriver)
    options = webdriver.ChromeOptions()

    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)

    if abstract.headless:
        options.add_argument('--headless')
        # options.add_argument('start-maximized') # Maximize Viewport
    options.add_argument('--no-sandbox')  # Bypass OS Security Model

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

    options.add_experimental_option("prefs", prefs)

    # Added for printing to PDF
    options.add_argument('--kiosk-printing')

    # driver = webdriver.Chrome(chromedriver, options=options)
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    return driver


def enable_download_in_headless_chrome(browser, abstract):
    document_directory = f'{abstract.target_directory}/Documents'

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


def create_webdriver(abstract):
    browser = chrome_webdriver(abstract)
    if abstract.headless:
        enable_download_in_headless_chrome(browser, abstract)
    return browser
