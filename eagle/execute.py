import os

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)

from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project,
                                      extrapolate_document_value,
                                      list_remaining_documents)
from settings.general_functions import get_county_data
from settings.import_list import generate_document_list
from settings.settings import web_directory
from settings.user_prompts import (continue_prompt, document_found,
                                   no_document_found, request_more_information)

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import next_result, record_document
from eagle.search import document_search


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document in document_list:
        document_search(browser, document)
        if open_document(browser, document):
            if document.number_results > 1:
                record_multiple_documents(browser, county, target_directory, abstract_dictionary, document_list, document, download)
            else:
                record_single_document(browser, county, target_directory, abstract_dictionary, document_list, document, download)
        else:
            record_bad_search(abstract_dictionary, document)
            no_document_found(document_list, document)
    return abstract_dictionary


def record_single_document(browser, county, target_directory, abstract_dictionary, document_list, document, download):
    document_number = record_document(browser, abstract_dictionary, document)
    if download:
        download_document(browser, county, target_directory, document_number)
    document_found(document_list, document)    


def record_multiple_documents(browser, county, target_directory, abstract_dictionary, document_list, document, download):
    record_single_document(browser, county, target_directory, abstract_dictionary, document_list, document, download)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        record_single_document(browser, county, target_directory, abstract_dictionary, document_list, document, download)


def review_multiple_documents(document_list, document):
    document_found(document_list, document, "review")
    for document in range(0, document.number_results):
        next_result(browser, document)
        document_found(document_list, document, "review")


def review_documents_from_list(browser, document_list):
    for document in document_list:
        document_search(browser, document)
        if open_document(browser, document):
            if document.number_results > 1:
                review_multiple_documents(document_list, document)
            else:
                document_found(document_list, document, "review")
        else:
            no_document_found(document_list, document, "review")


def create_abstraction(browser, county, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract_dictionary = search_documents_from_list(browser, county, target_directory, document_list, download)
    export_document(target_directory, file_name, abstract_dictionary)
    return abstract_dictionary


def execute_program(county, target_directory, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, False)
    county = get_county_data(county)
    account_login(browser)
    create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    while continue_prompt(target_directory, file_name, sheet_name):
        target_directory, file_name, sheet_name = \
            request_more_information(target_directory, file_name, sheet_name)
        create_abstraction(browser, county, target_directory, file_name, sheet_name, download)
    bundle_project(target_directory, file_name)
    browser.close()
    quit()


def execute_review(target_directory, file_name, sheet_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    review_documents_from_list(browser, document_list)
    browser.close()
    quit()


# def execute_web_program(client, legal, upload_file):
#     sheet_name = 'Documents'
#     download = False
#     file_name = upload_file
#     target_directory = web_directory
#     headless = False
#     browser = create_webdriver(target_directory, headless)
#     account_login(browser)
#     abstract_dictionary = create_abstraction(browser, target_directory, file_name, sheet_name, download)
#     browser.close()
#     return abstract_dictionary
