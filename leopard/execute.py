from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      create_document_directory,
                                      remaining_downloads)
from settings.general_functions import (get_county_data,
                                        javascript_script_execution, naptime)
from settings.import_list import generate_document_list
from settings.settings import web_directory

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

# from leopard.download import download_document
from leopard.leopard_variables import search_script
from leopard.login import account_login
from leopard.open_document import open_document
from leopard.record import record_document
from leopard.search import search


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document in document_list:
        search(browser, document)
        if open_document(browser, document):
            record_document(browser, dictionary, document)
            if download:
                if not download_document(browser, county, target_directory, document, document_number):
                    dictionary["Comments"][-1] = f'No document image located at reception number {document_number}.'
        #     print(f'Document located at reception number {document_number} recorded, '
        #           f'{remaining_downloads(document_list, document_number)} documents remaining.')
        #     javascript_script_execution(search_script)
        #     naptime()
        # else:
        #     record_bad_search(dictionary, document_number)
        #     print(f'No document found at reception number {document_number}, '
        #           f'{remaining_downloads(document_list, document_number)} documents remaining.')


def create_abstraction(browser, county, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    search_documents_from_list(browser, county, target_directory, document_list, download)
    return dictionary


def execute_program(headless, target_directory, county, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, headless)
    county = get_county_data(county)
    account_login(browser)
    # create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    # while continue_prompt(target_directory, file_name, sheet_name):
    #     target_directory, file_name, sheet_name = \
    #         request_more_information(target_directory, file_name, sheet_name)
    #     create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    browser.close()
    quit()
