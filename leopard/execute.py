from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      extrapolate_document_value,
                                      list_remaining_documents)
from settings.general_functions import (get_county_data,
                                        javascript_script_execution, naptime)
from settings.import_list import generate_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

from leopard.download import download_document
from leopard.leopard_variables import search_script
from leopard.login import account_login
from leopard.logout import logout
from leopard.open_document import open_document
from leopard.record import record_document
from leopard.search import search
from leopard.convert_document_numbers import convert_document_numbers


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document in document_list:
        search(browser, document)
        if open_document(browser, document):
            document_number = record_document(browser, dictionary, document)
            if download:
                if not download_document(browser, county, target_directory, document, document_number):
                    dictionary["Comments"][-1] = f'No document image located at {extrapolate_document_value(document)}'
            print(f'Document located at '
                  f'{extrapolate_document_value(document)} recorded, '
                  f'{list_remaining_documents(document_list, document)}')
            javascript_script_execution(browser, search_script)
            naptime()
        else:
            record_bad_search(dictionary, document)
            print(f'No document found at '
                  f'{extrapolate_document_value(document)}, '
                  f'{list_remaining_documents(document_list, document)}')


def review_documents_from_list(browser, document_list):
    for document in document_list:
        search(browser, document)
        if open_document(browser, document):
            input(f'Document located at {extrapolate_document_value(document)} located,'
                  'please review & press enter to continue...'
                  f'{list_remaining_documents(document_list, document)}')
            javascript_script_execution(search_script)
            naptime()
        else:
            input(f'No document found at {extrapolate_document_value(document)}, '
                  'please review & press enter to continue...'
                  f'{list_remaining_documents(document_list, document)}')


def create_abstraction(browser, county, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    convert_document_numbers(document_list)
    search_documents_from_list(browser, county, target_directory, document_list, download)
    return dictionary


def execute_program(headless, target_directory, county, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, headless)
    county = get_county_data(county)
    account_login(browser)
    create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    export_document(target_directory, file_name, dictionary)
    bundle_project(target_directory, file_name)
    logout(browser)
    browser.close()
    quit()


def execute_review(target_directory, file_name, sheet_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    convert_document_numbers(document_list)
    review_documents_from_list(browser, document_list)
    logout(browser)
    browser.close()
    quit()
