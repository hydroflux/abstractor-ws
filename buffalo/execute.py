#!/usr/bin/python3
from settings.abstract_object import abstract_dictionary
from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, document_found,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download

from buffalo.login import account_login
from buffalo.logout import logout
from buffalo.open_document import open_document
from buffalo.search import search


def record_single_document(browser, county, target_directory, document_list, document, start_time):
    pass


def handle_search_results(browser, county, target_directory, document_list, document, start_time):
    pass


def search_documents_from_list(browser, county, target_directory, document_list):
    pass


# Identical to crocodile execute_program
def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    dictionary = search_documents_from_list(browser, county, target_directory, document_list)
    logout(browser)
    abstraction = export_document(county, target_directory, file_name, dictionary)
    bundle_project(target_directory, abstraction)
    browser.close()
