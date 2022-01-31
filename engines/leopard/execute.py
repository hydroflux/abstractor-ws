#!/usr/bin/python3
from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

from engines.leopard.download import execute_download
from engines.leopard.login import account_login
from engines.leopard.logout import logout
from engines.leopard.open_document import open_document
from engines.leopard.record import next_result, record
from engines.leopard.search import search
from engines.leopard.transform import transform_document_list

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'tiger', 'jaguar', 'rattlesnake', & 'eagle' execute_program
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
        next_result
    )
    close_program(browser, abstract, logout)
