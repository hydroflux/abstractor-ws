#!/usr/bin/python3
from classes.Document import Document
# from engines.octopus.open_document import get_results, open_result
from project_management.export import export_document
# from project_management.timers import naptime
# from serializers.downloader import download_document

from serializers.executor import close_program

from settings.driver import create_webdriver

from engines.octopus.collect import collect
# from engines.octopus.download import execute_download
from engines.octopus.login import login
from engines.octopus.logout import logout
# from engines.octopus.open_document import open_document
# from engines.octopus.record import record
from engines.octopus.search import search


def execute_legal_search(abstract):
    browser = create_webdriver(abstract)
    document = Document("legal", abstract.legal, county=abstract.county)
    login(browser, abstract)
    search(browser, abstract, document)
    collect(browser, abstract)
    # result_links = get_results(browser, abstract, document)
    # for result in result_links[:5]:
    #     # naptime()
    #     open_result(browser, abstract, document, result)
    #     record(browser, abstract, document)
    #     download_document(browser, abstract, document, execute_download)
    #     # naptime()
    #     browser.back()
    project = export_document(abstract)
    project.bundle_project(abstract)
    close_program(browser, abstract, logout)


# Fix previous download issues
# build a legal search loop to build the document list and then search from list
