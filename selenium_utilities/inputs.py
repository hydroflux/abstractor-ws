from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium_utilities.element_interaction import center_element


def get_field_value(field):
    return field.get_attribute("value").strip()


def clear_input(browser, locator_function, attribute, type, document=None):
    try:
        while get_field_value(locator_function(browser, attribute, type, True, document)) != '':
            locator_function(browser, attribute, type, True, document).clear()
    except AttributeError:
        # print(f'Encountered an attribute error attempting to "clear input" for '
        #       f'{document.extrapolate_value()}, please review & press enter to continue...')
        print(f'Encountered an attribute error attempting to "clear input" for '
              f'{document.extrapolate_value()}, refreshing the page in order to try and continue.')
        browser.refresh()
        sleep(30)
        clear_input(browser, locator_function, attribute, type, document=None)
        # consider returning False or none & addressing the error handler


def enter_input_value(browser, locator_function, attribute, type, value, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != value:
        locator_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)


def click_button(browser, locator_function, attribute, type, document=None):
    button = locator_function(browser, attribute, type, True, document)
    while button is False:  # while loop added for eagle--might not be the most pure option
        browser.refresh()
        sleep(5)
        button = locator_function(browser, attribute, type, True, document)
    center_element(browser, button)
    button.click()
