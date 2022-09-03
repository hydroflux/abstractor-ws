#!/usr/bin/python3
from engines.platypus.collect import collect
from engines.platypus.download import execute_download
from engines.platypus.login import login
from engines.platypus.logout import logout
from engines.platypus.open_document import open_document
from engines.platypus.record import record
from engines.platypus.search import search

from serializers.executor import close_program, search_documents_from_list


def execute_legal_search(browser, abstract):
    login(browser, abstract)
    search(browser, abstract)
    collect(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download
    )
    close_program(browser, abstract, logout)
