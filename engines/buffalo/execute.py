#!/usr/bin/python3
from engines.buffalo.download import execute_download
from engines.buffalo.login import login
from engines.buffalo.logout import logout
from engines.buffalo.open_document import open_document
from engines.buffalo.record import record
from engines.buffalo.search import search
from engines.buffalo.navigation import next_result

from serializers.executor import close_program, search_documents_from_list


def execute_program(browser, abstract):
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
    close_program(browser, abstract, logout)
