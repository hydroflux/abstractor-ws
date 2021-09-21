from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import get_field_value, timeout


def locate_element_by_id(locator, document, id, type, clickable=False):
    try:
        if clickable:
            element_present = EC.element_to_be_clickable((By.ID, id))
        else:
            element_present = EC.presence_of_element_located((By.ID, id))
        WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_id(id)
        return element
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')


def locate_element_by_class_name(locator, document, class_name, type, clickable=False):
    try:
        if clickable:
            element_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        else:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
        WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_class_name(class_name)
        return element
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')


def locate_elements_by_class_name(locator, document, class_name, type, clickable=False):
    try:
        if clickable:
            elements_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        else:
            elements_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
        WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements_by_class_name(class_name)
        return elements
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')


def locate_element_by_tag_name(locator, document, tag_name, type, clickable=False):
    try:
        if clickable:
            element_present = EC.element_to_be_clickable((By.TAG_NAME, tag_name))
        else:
            element_present = EC.presence_of_element_located((By.TAG_NAME, tag_name))
        WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_tag_name(tag_name)
        return element
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')


def clear_input(browser, document, input_function, type, id):
    while get_field_value(input_function(browser, document, id, type)) != '':
        input_function(browser, document, id, type, True).clear()


def enter_input_value(browser, document, input_function, type, id, value):
    while get_field_value(input_function(browser, document, id, type)) != value:
        input_function(browser, document, id, type, True).send_keys(Keys.UP + value)


def click_button(browser, document, input_function, id, type):
    button = input_function(browser, document, id, type, True)
    button.click()
