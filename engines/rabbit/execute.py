#!/usr/bin/python3
from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

from engines.rabbit.download import execute_download
from engines.rabbit.login import login
# from engines.rabbit.logout import logout
# from engines.rabbit.navigation import next_result
from engines.rabbit.open_document import open_document
from engines.rabbit.record import record
from engines.rabbit.search import search


def execute_program(abstract):
    browser = create_webdriver(abstract)
    login(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download
        # next_result
    )
    close_program(browser, abstract)
