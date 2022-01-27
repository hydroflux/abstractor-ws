from actions.executors import close_program, handle_multiple_documents, handle_single_document
from engines.tiger.transform import transform_document_list
from settings.invalid import record_invalid_search
from settings.county_variables.tiger import search_script
from settings.driver import create_webdriver
from settings.general_functions import (javascript_script_execution, naptime, start_timer)

from engines.tiger.download import download_document
from engines.tiger.login import account_login
from engines.tiger.open_document import open_document
from engines.tiger.record import record
from engines.tiger.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'eagle', 'jaguar', & 'leopard' handle_search_results
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document, record, download_document)
        # These (below) are messy--need to move / update
        javascript_script_execution(search_script)
        naptime()
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document, record, download_document)


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


# Identical to 'leopard', 'jaguar', & 'eagle' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    close_program(browser, abstract)


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
