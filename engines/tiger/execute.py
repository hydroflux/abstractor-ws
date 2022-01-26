from settings.invalid import record_invalid_search
from settings.county_variables.tiger import search_script
from settings.driver import create_webdriver
from project_management.export import export_document
from settings.general_functions import (javascript_script_execution, naptime, start_timer)

from engines.tiger.download import download_document
from engines.tiger.login import account_login
from engines.tiger.open_document import open_document
from engines.tiger.record import record_document
from engines.tiger.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


def record_single_document(browser, abstract, document):
    record_document(browser, dataframe, document_number)
    if download:
        if not download_document(browser, county, target_directory, document_number):
            dataframe["Comments"][-1] = f'No document image located at reception number {document_number}.'
    print(f'Document located at reception number {document_number} recorded, '
            f'{remaining_downloads(document_list, document_number)} documents remaining.')
    javascript_script_execution(search_script)
    naptime()


def record_multiple_documents(browser, abstract, document):
    pass


def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        record_single_document(browser, abstract, document)
    elif document.number_results > 1:
        record_multiple_documents(browser, abstract, document)


# Identical to 'eagle', 'leopard', & 'jaguar' search_documents_from_list
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_invalid_search(abstract, document)
        # check_length(dataframe)  # Where is the best place to put this???


# Identical to 'leopard' execute_program
def execute_program(abstract):
    if abstract.download_only:
        abstract.headless = False  # Figure out better placement
    browser = create_webdriver(abstract)
    # transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    # logout(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()


# def execute_web_program(county, client, legal, upload_file):
#     county = get_county_data(county)
#     sheet_name = 'Documents'
#     file_name = upload_file
#     target_directory = web_directory
#     browser = create_webdriver(target_directory, False)
#     account_login(browser)
#     search_documents_from_list(browser, abstract)
#     export_document(target_directory, file_name, dataframe, client, legal)
#     bundle_project(target_directory, file_name)
#     browser.close()
#     return dataframe
