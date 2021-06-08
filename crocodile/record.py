from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import not_applicable
from settings.file_management import extrapolate_document_value
from settings.general_functions import assert_window_title

from crocodile.crocodile_variables import document_title


def record_document(browser, county, dictionary, document):
    assert_window_title(browser, document_title)