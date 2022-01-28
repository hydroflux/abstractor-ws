from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import download_button_id, view_group_id
from settings.download_management import previously_downloaded, update_download
from settings.initialization import prepare_for_download

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


# Very similar but not identical to 'jaguar' execute_download
# Identical to 'leopard' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, view_group_id,  # Open Download Submenu
                 "download submenu button", document)
    click_button(browser, locate_element_by_id, download_button_id,  # Execute Download
                 "execute download button", document)
    update_download(browser, abstract, document)


# Identical to 'eagle', 'tiger', & 'jaguar' download_document
def download_document(browser, abstract, document):
    prepare_for_download(abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
