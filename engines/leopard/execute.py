from settings.objects.abstract_dataframe import abstract_dictionary as dataframe
from settings.bad_search import no_document_image, record_bad_search
from settings.driver import create_webdriver
from project_management.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_found, no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from engines.leopard.download import download_document
from engines.leopard.login import account_login
from engines.leopard.logout import logout
from engines.leopard.open_document import open_document
from engines.leopard.record import next_result, record_document
from engines.leopard.search import search
from engines.leopard.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    document_number = record_document(browser, county, dataframe, document)
    if download:
        if not download_document(browser, county, target_directory, document, document_number):
            no_document_image(dataframe, document)
    document_found(start_time, document_list, document)


def download_single_document(browser, county, target_directory, document_list, document, start_time):
    document_number = get_reception_number(browser, document)
    if not download_document(browser, county, target_directory, document, document_number):
        no_document_image(dataframe, document)
    document_found(start_time, document_list, document, "download")


def record_multiple_documents(browser, county, target_directory, document_list, document, start_time):
    record_single_document(browser, county, target_directory, document_list, document, start_time)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        record_single_document(browser, county, target_directory, document_list, document, start_time)


def review_multiple_documents(browser, start_time, document_list, document):
    document_found(start_time, document_list, document, "review")
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        document_found(start_time, document_list, document, "review")


def download_multiple_documents(browser, county, target_directory, start_time, document_list, document):
    download_single_document(browser, county, target_directory, document)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        download_single_document(browser, county, target_directory, document)


def handle_search_results(browser, county, target_directory,
                          document_list, document, start_time, alt=None):
    if alt is None:
        if document.number_results > 1:
            record_multiple_documents(browser, county, target_directory,
                                      document_list, document, start_time)
        else:
            record_single_document(browser, county, target_directory,
                                   document_list, document, start_time)
    elif alt == 'review':
        if document.number_results > 1:
            review_multiple_documents(browser, start_time, document_list, document)
        else:
            document_found(start_time, document_list, document, "review")
    elif alt == "download":
        if document.number_results > 1:
            download_multiple_documents(browser, county, target_directory, start_time, document_list, document)
        else:
            download_single_document(browser, county, target_directory, document_list, document, start_time)


def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        # naptime()  # --- script runs without issues while this nap was in place
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_bad_search(abstract, document)
        # check_length(dataframe)  # Where is the best place to put this???


def review_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, False,
                                  document_list, document, start_time, "review")
        else:
            no_document_found(start_time, document_list, document, "review")


def download_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, True,
                                  document_list, document, start_time, "download")
        else:
            no_document_found(start_time, document_list, document)


def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    logout(browser)
    project = export_document(abstract)
    project.bundle_project(abstract)
    browser.close()


def execute_review(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    review_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    browser.close()


def execute_document_download(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    download_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    browser.close()
