from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      no_document_found)
from settings.general_functions import start_timer

from armadillo.login import account_login
from armadillo.logout import logout
from armadillo.open_document import open_document
from armadillo.record import record
from armadillo.search import search


def search_documents_from_list(browser, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            record(browser, dataframe, document)
        else:
            record_bad_search(dataframe, document)
            no_document_found(start_time, document_list, document)
        check_length(dataframe)
    return dataframe


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(browser, county, target_directory, document_list)
    )
    logout(browser)
    bundle_project(target_directory, abstraction)
    # browser.close()
