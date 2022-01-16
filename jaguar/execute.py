from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project, no_document_found
from settings.general_functions import start_timer

from jaguar.login import account_login
from jaguar.open_document import open_document
from jaguar.search import search
from jaguar.transform import transform_document_list


def handle_search_results(browser, target_directory, document_list, document):
    pass


def handle_bad_search(dataframe, document_list, document):
    record_bad_search(dataframe, document)
    no_document_found(document_list, document)


def search_documents_from_list(browser, target_directory, document_list):
    for document in document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(
                browser,
                target_directory,
                document_list,
                document
            )
        else:
            handle_bad_search(dataframe, document_list, document)
    return dataframe


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    transform_document_list(document_list, county)
    account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(
            browser,
            target_directory,
            document_list,
        )
    )
    bundle_project(target_directory, abstraction)
    browser.close()
