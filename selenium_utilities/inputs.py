from selenium.webdriver.common.keys import Keys


def get_field_value(field):
    return field.get_attribute("value").strip()


def clear_input(browser, document, input_function, type, id):
    while get_field_value(input_function(browser, document, id, type)) != '':
        input_function(browser, document, id, type, True).clear()


def enter_input_value(browser, document, input_function, type, id, value):
    while get_field_value(input_function(browser, document, id, type)) != value:
        input_function(browser, document, id, type, True).send_keys(Keys.UP + value)


def click_button(browser, document, input_function, id, type):
    button = input_function(browser, document, id, type, True)
    button.click()
