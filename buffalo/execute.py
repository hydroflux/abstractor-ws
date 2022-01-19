#!/usr/bin/python3
from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_found,
                                      extrapolate_document_value,
                                      no_document_found)
from settings.general_functions import start_timer

from buffalo.login import account_login
from buffalo.logout import logout
from buffalo.open_document import open_document
from buffalo.search import search


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    pass
    document_found(start_time, document_list, document)


def handle_search_results(browser, county, target_directory, document_list, document, start_time):
    if document.number_results == 1:
        record_single_document(browser, county, target_directory, document_list, document, start_time)
    elif document.number_results > 1:
        print(f'Browser located multiple results for '
              f'{extrapolate_document_value(document)}; '
              f'No currently process built to handle multiple documents, please review.')
        input()


# Identical to crocodile search_documents_from_list
def search_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, document_list, document, start_time)
        else:
            record_bad_search(dataframe, document)
            no_document_found(start_time, document_list, document)
        check_length(dataframe)
    return dataframe


# Identical to crocodile execute_program
def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    dataframe = search_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dataframe)
    bundle_project(target_directory, abstraction)
    browser.close()
