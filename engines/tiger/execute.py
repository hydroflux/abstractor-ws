from serializers.executor import close_program, search_documents_from_list
from engines.tiger.transform import transform_document_list
from settings.driver import create_webdriver

from engines.tiger.download import execute_download
from engines.tiger.login import account_login
from engines.tiger.open_document import open_document
from engines.tiger.record import record
from engines.tiger.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'leopard', 'jaguar', 'rattlesnake', & 'eagle' execute_program
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
        execute_download,
        next_result=None
    )
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
