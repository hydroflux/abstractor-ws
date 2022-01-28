#!/usr/bin/python3
from actions.executors import close_program, handle_search_results, search_documents_from_list
from settings.invalid import record_invalid_search
from settings.driver import create_webdriver
from settings.general_functions import start_timer

from engines.eagle.download import download_document
from engines.eagle.login import account_login
from engines.eagle.open_document import open_document
from engines.eagle.record import next_result, record
from engines.eagle.search import search
from engines.eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'leopard', 'jaguar', & 'tiger' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        download_document,
        next_result
    )
    close_program(browser, abstract)


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
