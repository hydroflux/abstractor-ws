from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from crocodile.crocodile_variables import search_title, search_url


def open_search(browser):
    browser.get(search_url)
    assert search_title


def enter_document_number(browser, document):
    pass


def execute_search(browser):
    pass


def document_search(browser, document):
    open_search(browser)
    enter_document_number(browser, document)
    execute_search(browser)
