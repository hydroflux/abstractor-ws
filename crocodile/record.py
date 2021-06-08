from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import not_applicable
from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, get_element_text,
                                        timeout, title_strip)

from crocodile.crocodile_variables import (document_information_class,
                                           document_title, general_information_id)


def locate_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.CLASS_NAME, document_information_class))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_class_name(document_information_class)
        return document_information
    except TimeoutException:
        print(f'Browser timed out trying to locate document page information for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_general_information(document_information, document):
    try:
        general_information_present = EC.presence_of_element_located((By.ID, general_information_id))
        WebDriverWait(document_information, timeout).until(general_information_present)
        general_information = document_information.find_element_by_id(general_information_id)
        return general_information
    except TimeoutException:
        print(f'Browser timed out trying to locate general information for '
              f'{extrapolate_document_value(document)}')


def record_general_information(document_information, document):
    pass


def locate_party_information(document_information, document):
    pass


def locate_party_and_property_information(document_information, document):
    pass


def record_party_and_property_information(document_information, document):
    pass


def record_related_document_information(document_information, document):
    pass


def record_document(browser, county, dictionary, document):
    assert_window_title(browser, document_title)
    document_information = locate_document_information(browser, document)
    document_number = record_general_information(document_information, document)
    record_party_and_property_information(document_information, document)
    record_related_document_information(document_information, document)
    return document_number
