from selenium.webdriver.common.keys import Keys


def get_field_value(field):
    return field.get_attribute("value").strip()


def clear_input(browser, input_function, attribute, type, document=None):
    while get_field_value(input_function(browser, attribute, type, True, document)) != '':
        input_function(browser, attribute, type, True, document).clear()


def enter_input_value(browser, input_function, attribute, type, value, document=None):
    while get_field_value(input_function(browser, attribute, type, True, document)) != value:
        input_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)


def click_button(browser, input_function, attribute, type, document=None):
    button = input_function(browser, attribute, type, True, document)
    button.click()
