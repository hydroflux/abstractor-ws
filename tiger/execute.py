from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search
from settings.county_variables.tiger import search_script
from settings.driver import create_webdriver
from project_management.export import export_document
from settings.file_management import bundle_project, remaining_downloads
from settings.general_functions import (get_county_data,
                                        javascript_script_execution, naptime)
from project_management.import_list import generate_document_list
from settings.settings import download, web_directory

from tiger.download import download_document
from tiger.login import account_login
from tiger.open_document import open_document
from tiger.record import record_document
from tiger.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document():
    pass


def record_multiple_documents():
    pass


def review_multiple_documents():
    pass


def handle_search_results():
    pass


def search_documents_from_list(browser, county, target_directory, document_list):
    for document_number in document_list:
        search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, dataframe, document_number)
            if download:
                if not download_document(browser, county, target_directory, document_number):
                    dataframe["Comments"][-1] = f'No document image located at reception number {document_number}.'
            print(f'Document located at reception number {document_number} recorded, '
                  f'{remaining_downloads(document_list, document_number)} documents remaining.')
            javascript_script_execution(search_script)
            naptime()
        else:
            record_bad_search(dataframe, document_number)
            print(f'No document found at reception number {document_number}, '
                  f'{remaining_downloads(document_list, document_number)} documents remaining.')


def review_documents_from_list():
    pass


def create_abstraction(browser, county, target_directory, file_name, sheet_name):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    search_documents_from_list(browser, county, target_directory, document_list)
    return dataframe


def execute_program():
    pass


def execute_review():
    pass


def execute_web_program(county, client, legal, upload_file):
    county = get_county_data(county)
    sheet_name = 'Documents'
    file_name = upload_file
    target_directory = web_directory
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    dataframe = create_abstraction(browser, county, target_directory, file_name, sheet_name)
    export_document(target_directory, file_name, dataframe, client, legal)
    bundle_project(target_directory, file_name)
    browser.close()
    return dataframe
