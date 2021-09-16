#!/usr/bin/python3
from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from eagle.download import download_document
from eagle.login import account_login
from eagle.open_document import open_document
from eagle.record import next_result, record_document
from eagle.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, county, document_list, document, start_time, review):
    record_document(browser, county, dataframe, document)  # why does county need to be passed in
    document_found(start_time, document_list, document, review)


# def review_multiple_documents(browser, start_time, document_list, document):
#     document_found(start_time, document_list, document, "review")
#     for document_instance in range(0, (document.number_results - 1)):
#         next_result(browser, document)
#         document_found(start_time, document_list, document, "review")


# def record_multiple_documents(browser, county, target_directory,
#                               dataframe, document_list, document, start_time):
#     record_single_document(browser, county, target_directory, document_list, document, start_time)
#     for _ in range(0, (document.number_results - 1)):
#         next_result(browser, document)
#         record_single_document(browser, county, target_directory,
#                                dataframe, document_list, document, start_time)


def download_single_document(browser, county, target_directory, document_list, document):
    # document_number = get_reception_number(browser, document)
    if not download_document(
        browser,
        county,
        dataframe,
        target_directory,
        document
    ):  # add document reception number to document instance
        unable_to_download(dataframe, document)
        no_document_downloaded(document_list, document)
    else:
        document_downloaded(document_list, document)
        # document_found(start_time, document_list, document)
        # => this is probably a leftover from 'download document list'


# def download_multiple_documents(browser, county, target_directory, document_list, document, start_time):
#     download_single_document(browser, county, target_directory, document_list, document, start_time)
#     for document_instance in range(0, (document.number_results - 1)):
#         next_result(browser, document)
#         download_single_document(browser, county, target_directory, document_list, document, start_time)


def handle_single_document(browser, county, target_directory, document_list, document, start_time, review):
    record_single_document(
        browser,
        county,
        document_list,
        document,
        start_time,
        review
    )
    if download and not review:
        download_single_document(
            browser,
            county,
            target_directory,
            document_list,
            document
        )


def handle_multiple_documents(browser, county, target_directory, document_list, document, start_time, review):
    handle_single_document(
        browser,
        county,
        target_directory,
        document_list,
        document,
        start_time,
        review
    )
    for _ in range(0, (document.number_results - 1)):
        next_result(browser, document)
        handle_single_document(
            browser,
            county,
            target_directory,
            document_list,
            document,
            start_time,
            review
        )


def handle_search_results(browser, county, target_directory,
                          document_list, document, start_time, review):
    if document.number_results == 1:
        handle_single_document(
            browser,
            county,
            target_directory,
            document_list,
            document,
            start_time,
            review
        )
    elif document.number_results > 1:
        handle_multiple_documents(
            browser,
            county,
            target_directory,
            document_list,
            document,
            start_time,
            review
        )
    # elif alt == 'review':
    #     if document.number_results > 1:
    #         review_multiple_documents(browser, start_time, document_list, document)
    #     else:
    #         document_found(start_time, document_list, document, "review")
    # elif alt == "download":
    #     if document.number_results > 1:
    #         download_multiple_documents(browser, county, target_directory, document_list, document, start_time)
    #     else:
    #         download_single_document(browser, county, target_directory, document_list, document, start_time)


def search_documents_from_list(browser, county, target_directory, document_list, review):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(
                browser,
                county,
                target_directory,
                document_list,
                document,
                start_time,
                review
            )
        else:
            record_bad_search(dataframe, document)
            no_document_found(start_time, document_list, document, review)
        check_length(dataframe)
    return dataframe  # Is this necessary ? ? ?


# def create_abstraction(browser, county, target_directory, document_list, file_name):
#     dataframe = search_documents_from_list(browser, county, target_directory, document_list)
#     # Is the dataframe return necessary ? ? ?
#     return export_document(county, target_directory, file_name, dataframe)


def execute_program(county, target_directory, document_list, file_name, review=False):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(
            browser,
            county,
            target_directory,
            document_list,
            review
        )

    )
    # logout ???
    # create_abstraction(browser, county, target_directory, document_list, file_name)
    bundle_project(target_directory, abstraction)
    browser.close()


# def review_documents_from_list(browser, county, target_directory, document_list):
#     for document in document_list:
#         start_time = start_timer()
#         search(browser, document)
#         if open_document(browser, document):
#             handle_search_results(browser, county, target_directory,
#                                   document_list, document, start_time, 'review')
#         else:
#             no_document_found(start_time, document_list, document, "review")


def download_documents_from_list(browser, county, target_directory, document_list):
    for document in document_list:
        start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, county, target_directory,
                                  document_list, document, start_time, 'download')
        else:
            no_document_found(start_time, document_list, document)


# def execute_review(county, target_directory, document_list):
#     browser = create_webdriver(target_directory, False)
#     account_login(browser)
#     review_documents_from_list(browser, county, target_directory, document_list)
#     browser.close()


def execute_document_download(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    download_documents_from_list(browser, county, target_directory, document_list)
    browser.close()


# def execute_web_program(client, legal, upload_file):
#     sheet_name = 'Documents'
#     download = False
#     file_name = upload_file
#     target_directory = web_directory
#     headless = False
#     browser = create_webdriver(target_directory, headless)
#     account_login(browser)
#     dataframe = create_abstraction(browser, target_directory, file_name, sheet_name, download)
#     browser.close()
#     return abstract_dictionary
