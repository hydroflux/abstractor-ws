#!/usr/bin/python3
from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

# from engines.octopus.download import execute_download
from engines.octopus.login import login
from engines.octopus.logout import logout
# from engines.octopus.navigation import next_result
# from engines.octopus.open_document import open_document
# from engines.octopus.record import record
# from engines.octopus.search import search


def execute_program(abstract):
    browser = create_webdriver(abstract)
    login(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        # search,
        # open_document,
        # record,
        # execute_download,
        # next_result
    )
    close_program(browser, abstract, logout)
