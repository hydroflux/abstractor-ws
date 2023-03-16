from project_management.timers import naptime

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.general_functions import javascript_script_execution


def handle_disclaimer(browser, abstract):
    javascript_script_execution(browser, abstract.county.scripts["Open Search"])
    disclaimer = locate_element_by_id(browser, abstract.county.ids["Disclaimer"], "disclaimer")
    if disclaimer.get_attribute('class') == abstract.county.classes["Disclaimer Active"]:
        click_button(browser, locate_element_by_id,
                     abstract.county.buttons["Disclaimer"], "disclaimer button")
        naptime()
