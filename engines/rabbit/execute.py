#!/usr/bin/python3
from engines.rabbit.download import execute_download
from engines.rabbit.login import login
from engines.rabbit.name_search import name_search
from engines.rabbit.open_document import open_document
from engines.rabbit.record import record
from engines.rabbit.search import search

from project_management.export import export_document

from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver


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


def execute_name_search(abstract):
    browser = create_webdriver(abstract)
    login(browser, abstract)
    name_search(browser, abstract)
    project = export_document(abstract)
    project.bundle_project(abstract)
    close_program(browser, abstract)
