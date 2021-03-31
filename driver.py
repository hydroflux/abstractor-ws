from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Look into how to change driver preferences mid script -- for download directories
def chrome_webdriver(target_directory, headless):
    chromedriver = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()

    # options.add_argument('start-maximized') # Maximize Viewport
    options.add_argument('--no-sandbox')  # Bypass OS Security Model

    prefs = {
        # "download.default_directory": f'{target_directory}/Documents',
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chromedriver, options=options)
    driver.maximize_window()

    return driver


def enable_download_in_headless_chrome(browser, target_directory):
    document_directory = f'{target_directory}/Downloads'
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


def create_webdriver(target_directory, headless):
    browser = chrome_webdriver(target_directory, headless)
    if headless:
        enable_download_in_headless_chrome(browser, target_directory)
    return browser
