from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.tiger import download_button_id, view_panel_id

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


# Very similar but not identical to 'jaguar' execute_download
# Identical to 'leopard' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, view_panel_id,  # Open Download Submenu
                 "download submenu button", document)
    click_button(browser, locate_element_by_id, download_button_id,  # Execute Download
                 "execute download button", document)
