from rattlesnake.validation import verify_document_description_page_loaded
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def locate_document_description_table():
    pass


def record_grantor():
    pass


def record_grantee():
    pass


def record_book():
    pass


def record_page():
    pass


def record_reception_number():
    pass


def record_document_type():
    pass


def record_effective_date():
    pass


def record_recording_date():
    pass


def record_legal():
    pass


def record_related_documents():
    pass


def record_comments():
    pass


def aggregate_document_information():
    pass


def record_document_fields():
    pass


def record(browser, document):
    verify_document_description_page_loaded(browser, document)