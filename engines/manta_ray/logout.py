from selenium_utilities.inputs import click_button
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_elements_by_class_name)

# Exact same functionality in "dolphin", "manta_ray", "octopus", & "swordfish"


def open_logout_dropdown(browser, abstract):
    dropdown_buttons = locate_elements_by_class_name(browser, abstract.county.buttons["Logout Dropdown"],
                                                     "logout dropdown", True)
    dropdown_buttons[1].click()


def logout(browser, abstract):
    open_logout_dropdown(browser, abstract)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Logout"], "logout button", True)
