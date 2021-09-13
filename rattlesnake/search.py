from rattlesnake.validation import verify_document_search_page_loaded
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (assert_window_title, get_field_value,
                                        javascript_script_execution, timeout)

from armadillo.armadillo_variables import (document_search_field_id,
                                           document_search_title,
                                           document_search_url,
                                           execute_document_search_script)


# Matched armadillo open_document_search
def open_document_search(browser, document):
    browser.get(document_search_url)
    verify_document_search_page_loaded(browser, document)


def locate_document_search_field():
    pass


def clear_document_search_field():
    pass


def enter_document_number():
    pass


def handle_document_search_field():
    pass


def document_search():
    pass


def search():
    pass
