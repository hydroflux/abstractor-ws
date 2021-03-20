from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def chrome_webdriver(target_directory):
    chromedriver = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()

    options.add_argument('start-maximized') # Maximize Viewport
    options.add_argument('--no-sandbox') # Bypass OS Security Model

    preferences = {
        "download.default_directory": target_directory,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }

    options.add_experimental_option("preferences", preferences)

    return webdriver.Chrome(chromedriver, options=options)