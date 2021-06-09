from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project
from settings.general_functions import start_timer
from settings.user_prompts import document_found, no_document_found


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    pass


def record_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    pass


def handle_search_results(browser, county, target_directory, download, document_list, document, start_time):
    pass


def search_documents_from_list(browser, county, target_directory, document_list, download):
    pass


def execute_program(county, target_directory, document_list, file_name, download):
    pass
