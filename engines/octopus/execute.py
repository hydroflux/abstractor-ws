#!/usr/bin/python3
from classes.Document import Document
from engines.octopus.open_document import get_results, open_result
from project_management.export import export_document

from serializers.executor import close_program

from settings.driver import create_webdriver

# from engines.octopus.download import execute_download
from engines.octopus.login import login
from engines.octopus.logout import logout
# from engines.octopus.navigation import next_result
# from engines.octopus.open_document import open_document
# from engines.octopus.record import record
from engines.octopus.search import search


def execute_legal_search(abstract):
    browser = create_webdriver(abstract)
    document = Document("legal", abstract.legal)
    login(browser, abstract)
    search(browser, abstract, document)
    result_links = get_results(browser, abstract, document)
    for result in result_links:
        # naptime()
        open_result(browser, abstract, document, result)
        # record
        # download
        browser.back()
        # naptime()
    project = export_document(abstract)
    project.bundle_project(abstract)
    close_program(browser, abstract, logout)
