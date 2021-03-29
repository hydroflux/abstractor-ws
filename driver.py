from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Look into how to change driver preferences mid script -- for download directories
def chrome_webdriver(target_directory):
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
