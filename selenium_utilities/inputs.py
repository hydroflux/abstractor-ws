from selenium.webdriver.common.keys import Keys


def get_field_value(field):
    return field.get_attribute("value").strip()


def clear_input(browser, locator_function, attribute, type, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != '':
        locator_function(browser, attribute, type, True, document).clear()


def enter_input_value(browser, locator_function, attribute, type, value, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != value:
        locator_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)


def click_button(browser, locator_function, attribute, type, document=None):
    button = locator_function(browser, attribute, type, True, document)
    button.click()
