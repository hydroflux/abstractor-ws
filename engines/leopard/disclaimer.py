from project_management.timers import naptime

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (disclaimer_active_class,
                                               disclaimer_button_id,
                                               disclaimer_id, open_script)
from settings.general_functions import javascript_script_execution


def handle_disclaimer(browser):
    javascript_script_execution(browser, open_script)
    disclaimer = locate_element_by_id(browser, disclaimer_id, "disclaimer", False)
    if disclaimer.get_attribute('class') == disclaimer_active_class:
        click_button(browser, locate_element_by_id, disclaimer_button_id, "disclaimer button")
        naptime()
