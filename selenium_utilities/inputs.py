from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

from selenium_utilities.element_interaction import center_element
from settings.initialization import convert_to_mmddyyyy


# Similar code is used in element_interaction.py and locators.py (but not cleaned up) - consider removing from here
def get_field_value(field):
    return field.get_attribute("value").strip()


def access_input_field(browser, locator_function, attribute, type, document):
    count = 0
    while locator_function(browser, attribute, type, True, document) is None:
        browser.save_screenshot(f'access_input_field_error_{attribute}_{type}.png')
        count += 1
        browser.refresh()
        sleep(30)
        if count == 5:
            input(f'Unable to access input field for "{document.extrapolate_value()}", '
                  'please review & press enter to continue...')
    return locator_function(browser, attribute, type, True, document)


def clear_input(browser, locator_function, attribute, type, document=None):
    input_field = access_input_field(browser, locator_function, attribute, type, document)
    while get_field_value(input_field) != '':
        center_element(browser, input_field)
        input_field.clear()
        # clear_field_value(browser, input_field, attribute, type, document)


def enter_input_value(browser, locator_function, attribute, type, value, document=None):
    field_value = get_field_value(locator_function(browser, attribute, type, True, document))
    while field_value != value:
        # add a 'scroll_into_view' or 'center_element' function
        if len(field_value) != len(value):
            clear_input(browser, locator_function, attribute, type, document)
        locator_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)
        field_value = get_field_value(locator_function(browser, attribute, type, True, document))


def click_elsewhere(browser):
    ActionChains(browser).move_by_offset(10, 10).click().perform()


def enter_datepicker_value(browser, locator_function, attribute, type, value, document=None):
    field_value = get_field_value(locator_function(browser, attribute, type, True, document))
    converted_field_value = convert_to_mmddyyyy(field_value)
    while converted_field_value != value:
        # add a 'scroll_into_view' or 'center_element' function
        field_input = locator_function(browser, attribute, type, True, document)
        field_input.send_keys(Keys.END + Keys.SHIFT + Keys.UP)
        field_input.send_keys(value)
        click_elsewhere(browser)
        field_value = get_field_value(locator_function(browser, attribute, type, True, document))
        converted_field_value = convert_to_mmddyyyy(field_value)


def click_button(locator, locator_function, attribute, type, document=None, quick=False):
    try:
        attempts = 0
        button = locator_function(locator, attribute, type, True, document, quick)
        while button is False and attempts < 3:
            attempts += 1
            print(f'Unable to locate "{type}" button, trying again ({attempts} of 4)...')
            button = locator_function(locator, attribute, type, True, document, quick)

        if button is False:
            if document is None:
                input(f'Unable to locate "{type}" button, please review and press enter to continue.')
            else:
                input(f'Unable to locate "{type}" button for {document.extrapolate_value()}, '
                      f'please review and press enter to continue.')
            button = locator_function(locator, attribute, type, True, document, quick)

        if not isinstance(locator, WebElement):
            center_element(locator, button)
        button.click()
    except ElementClickInterceptedException:  # handles an issue with eagle downloads
        print(f'Element click intercepted while trying to click "{type}" '
              f'attribute "{attribute}", please review and press enter to continue...')
        input()
        return False
