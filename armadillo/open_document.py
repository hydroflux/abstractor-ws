from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import document_value, extrapolate_document_value
from settings.general_functions import assert_window_title, timeout

from armadillo.armadillo_variables import number_results_class, search_results_id, document_search_results_title


def verify_successful_search(browser, document):
    if not assert_window_title(browser, document_search_results_title):
        print(f'Browser failed to successfully execute search for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def count_results(browser, document):
    pass # assert_window_title


def verify_result_count(browser, document):
    pass


def open_document(browser, document):
    verify_successful_search(browser, document)
