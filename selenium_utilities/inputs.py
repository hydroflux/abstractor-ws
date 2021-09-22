from selenium.webdriver.common.keys import Keys


def get_field_value(field):
    return field.get_attribute("value").strip()


def center_element(browser, element):
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = browser.execute_script('return window.innerHeight')
    window_y = browser.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y
    browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def clear_input(browser, locator_function, attribute, type, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != '':
        locator_function(browser, attribute, type, True, document).clear()


def enter_input_value(browser, locator_function, attribute, type, value, document=None):
    while get_field_value(locator_function(browser, attribute, type, True, document)) != value:
        locator_function(browser, attribute, type, True, document).send_keys(Keys.UP + value)


def click_button(browser, locator_function, attribute, type, document=None):
    button = locator_function(browser, attribute, type, True, document)
    center_element(browser, button)
    button.click()
