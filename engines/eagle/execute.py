#!/usr/bin/python3
from engines.eagle.name_search import name_search
from project_management.export import export_document
from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

from engines.eagle.download import execute_download
from engines.eagle.login import login
from engines.eagle.navigation import next_result
from engines.eagle.open_document import open_document
from engines.eagle.record import record
from engines.eagle.search import search

# from engines.eagle.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'leopard', 'jaguar', 'rattlesnake', & 'tiger' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    # transform_document_list(abstract)
    login(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download,
        next_result
    )
    close_program(browser, abstract)


def execute_name_search(abstract):
    browser = create_webdriver(abstract)
    login(browser, abstract)
    name_search(browser, abstract)
    project = export_document(abstract)
    project.bundle_project(abstract)
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
