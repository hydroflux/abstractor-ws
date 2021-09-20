from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import get_field_value, timeout


def locate_element_by_id(browser, document, id, type):
    try:
        input_present = EC.element_to_be_clickable((By.ID, id))
        WebDriverWait(browser, timeout).until(input_present)
        input = browser.find_element_by_id(id)
        return input
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" input for '
              f'{document.extrapolate_value()}.')


def locate_element_by_class_name(browser, document, class_name, type):
    try:
        element_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        WebDriverWait(browser, timeout).until(element_present)
        element = browser.find_element_by_class_name(class_name)
        return element
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" input for '
              f'{document.extrapolate_value()}.')


def locate_elements_by_class_name(browser, document, class_name, type):
    try:
        elements_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        WebDriverWait(browser, timeout).until(elements_present)
        elements = browser.find_elements_by_class_name(class_name)
        return elements
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" input for '
              f'{document.extrapolate_value()}.')


def clear_input(browser, document, input_function, type, id):
    while get_field_value(input_function(browser, document, id, type)) != '':
        input_function(browser, document, id, type).clear()


def enter_input_value(browser, document, input_function, type, id, value):
    while get_field_value(input_function(browser, document, id, type)) != value:
        input_function(browser, document, id, type).send_keys(Keys.UP + value)


def click_button(browser, document, input_function, id, type):
    button = input_function(browser, document, id, type)
    button.click()
