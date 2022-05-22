#!/usr/bin/python3
from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

from engines.jaguar.download import execute_download
from engines.jaguar.login import login
from engines.jaguar.navigation import next_result
from engines.jaguar.open_document import open_document
from engines.jaguar.record import record
from engines.jaguar.search import search


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
    close_program(browser, abstract)
