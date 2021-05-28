from settings.abstract_object import abstract_dictionary as dictionary
from settings.bad_search import no_document_image, record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project, check_length
from settings.general_functions import start_timer
from settings.user_prompts import document_found, no_document_found

from leopard.download import download_document
from leopard.login import account_login
from leopard.logout import logout
from leopard.open_document import open_document
from leopard.record import next_result, record_document
from leopard.search import search
from leopard.transform_document_list import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, county, target_directory, download, document_list, document, start_time):
    document_number = record_document(browser, county, dictionary, document)
    if download:
        if not download_document(browser, county, target_directory, document, document_number):
            no_document_image(dictionary, document)
    document_found(start_time, document_list, document)


def download_single_document(browser, county, target_directory, document, document_number):
    if not download_document(browser, county, target_directory, document, document_number):
        no_document_image(dictionary, document)
    # document_found(start_time, document_list, document, "download")


def record_multiple_documents(browser, county, target_directory, download, document_list, document, start_time):
    record_single_document(browser, county, target_directory, download, document_list, document, start_time)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        record_single_document(browser, county, target_directory, download, document_list, document, start_time)


def review_multiple_documents(browser, start_time, document_list, document):
    document_found(start_time, document_list, document, "review")
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        document_found(start_time, document_list, document, "review")


def download_multiple_documents(browser, county, target_directory, start_time, document_list,
                                document, document_number):
    download_single_document(browser, county, target_directory, document, document_number)
    for document_instance in range(0, (document.number_results - 1)):
        next_result(browser, document)
        download_single_document(browser, county, target_directory, document, document_number)


def handle_search_results(browser, county, target_directory, download,
                          document_list, document, start_time, alt=None):
    if alt is None:
        if document.number_results > 1:
            record_multiple_documents(browser, county, target_directory, download,
                                      document_list, document, start_time)
        else:
            record_single_document(browser, county, target_directory, download,
                                   document_list, document, start_time)
    elif alt == 'review':
        if document.number_results > 1:
            review_multiple_documents(browser, start_time, document_list, document)
        else:
            document_found(start_time, document_list, document, "review")
    elif alt == "download":
        document_number = record_document(browser, county, dictionary, document)
        if document.number_results > 1:
            download_multiple_documents(browser, county, target_directory, start_time,
                                        document_list, document, document_number)
        else:
            # This is unnecessary & doesn't make sense just to get the document number out
            if not download_document(browser, county, target_directory, document, document_number):
                no_document_image(dictionary, document)
            # document_found(start_time, document_list, document, "download")


def search_documents_from_list(browser, county, target_directory, document_list, download):
    transform_document_list(document_list)
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        # naptime()  # --- script runs without issues while this nap was in place
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, download,
                                  document_list, document, start_time)
        else:
            record_bad_search(dictionary, document)
            no_document_found(start_time, document_list, document)
        check_length(dictionary)
    return dictionary


def review_documents_from_list(browser, county, target_directory, document_list):
    transform_document_list(document_list)
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, False,
                                  document_list, document, start_time, "review")
        else:
            no_document_found(document_list, document, "review")


def download_documents_from_list(browser, county, target_directory, document_list):
    transform_document_list(document_list)
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory, True,
                                  document_list, document, start_time, "download")
        else:
            no_document_found(document_list, document, "download")


def execute_program(headless, county, target_directory, document_list, file_name, sheet_name, download):
    browser = create_webdriver(target_directory, headless)
    account_login(browser)
    dictionary = search_documents_from_list(browser, county, target_directory, document_list, download)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dictionary)
    bundle_project(target_directory, abstraction, download)
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
