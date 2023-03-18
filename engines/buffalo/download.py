from engines.buffalo.frame_handling import (switch_to_download_frame,
                                            switch_to_download_submenu_frame)
from engines.buffalo.validation import check_for_download_alert

from project_management.timers import micro_nap

from selenium_utilities.locators import locate_element


def open_download_submenu(browser, abstract, document):
    switch_to_download_submenu_frame(browser, abstract)
    download_submenu_button = locate_element(browser, "id", abstract.county.buttons["Download Submenu"],
                                             "download submenu button", True, document)
    download_submenu_button.click()


def download_document(browser, abstract, document):
    switch_to_download_frame(browser, abstract)
    download_button = locate_element(browser, "xpath", abstract.county.buttons["Download"],
                                     "download button", True, document)
    download_button.click()


def execute_download(browser, abstract, document):
    open_download_submenu(browser, abstract, document)
    micro_nap()
    if not check_for_download_alert(browser, abstract, document):
        download_document(browser, abstract, document)
