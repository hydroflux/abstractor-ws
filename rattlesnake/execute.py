from settings.abstract_object import abstract_dictionary as dataframe
from settings.bad_search import record_bad_search, unable_to_download
from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import (bundle_project, check_length,
                                      document_downloaded, document_found,
                                      extrapolate_document_value,
                                      no_document_downloaded,
                                      no_document_found)
from settings.general_functions import start_timer
from settings.settings import download, headless


def execute_program(county, target_directory, document_list, file_name, review=False):
    browser = create_webdriver(target_directory, headless)
    # transform
    # login
    # create document
    # logout
    # bundle
    # close
