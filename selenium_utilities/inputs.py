from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from time import sleep

from selenium_utilities.element_interaction import center_element


def get_field_value(field):
    return field.get_attribute("value").strip()


def clear_input(browser, locator_function, attribute, type, document=None):
    try:
        while get_field_value(locator_function(browser, attribute, type, True, document)) != '':
            # add a 'scroll_into_view' or 'center_element' function
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


# Enter input value should include 'clearing' as part of its functionality
# => get rid of 'clear_search' functions altogether by simply clearing any input before updating
def enter_input_value(browser, locator_function, attribute, type, value, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != value:
        # add a 'scroll_into_view' or 'center_element' function
        locator_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)


def click_button(browser, locator_function, attribute, type, document=None):
    try:
        button = locator_function(browser, attribute, type, True, document)
        if button is False:
            return False
        else:
            center_element(browser, button)
            button.click()
    except ElementClickInterceptedException:  # handles an issue with eagle downloads
        print(f'Element click intercepted while trying to click "{type}" '
              f'attribute "{attribute}", please review and press enter to continue...')
        input()
        return False
