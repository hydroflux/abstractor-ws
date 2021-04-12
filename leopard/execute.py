from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import no_document_image, record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      extrapolate_document_value,
                                      list_remaining_documents)
from settings.general_functions import (get_county_data,
                                        javascript_script_execution, naptime)
from settings.import_list import generate_document_list
from settings.user_prompts import document_found, no_document_found

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

from leopard.convert_document_numbers import convert_document_numbers
from leopard.download import download_document
from leopard.leopard_variables import search_script
from leopard.login import account_login
from leopard.logout import logout
from leopard.open_document import open_document
from leopard.record import record_document
from leopard.search import search


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document in document_list:
        search(browser, document)
        if open_document(browser, document):
            document_number = record_document(browser, dictionary, document)
            if download:
                if not download_document(browser, county, target_directory, document, document_number):
                    no_document_image(dictionary, document)
            document_found(document_list, document)
            javascript_script_execution(browser, search_script)
            naptime()
        else:
            record_bad_search(dictionary, document)
            no_document_found(document_list, document)


def review_documents_from_list(browser, document_list):
    for document in document_list:
        search(browser, document)
        if open_document(browser, document):
            document_found(document_list, document, "review")
            javascript_script_execution(browser, search_script)
            naptime()
        else:
            no_document_found(document_list, document, "review")


def create_abstraction(browser, county, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    convert_document_numbers(document_list)
    search_documents_from_list(browser, county, target_directory, document_list, download)
    return dictionary


def execute_program(headless, target_directory, county, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, headless)
    county = get_county_data(county)
    account_login(browser)
    dictionary = create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
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
