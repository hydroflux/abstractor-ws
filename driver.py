from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def chrome_webdriver(document_directory):
    chromedriver = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()

    options.add_argument('start-maximized') # Maximize Viewport
    options.add_argument('--no-sandbox') # Bypass OS Security Model

    prefs = {
        "download.default_directory": document_directory,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }

    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(chromedriver, options=options)