from datetime import datetime
from pprint import pprint
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.keys import Keys
from project_management.timers import short_nap


# Is this function being used in any capacity?
def bell():
    print("\a")


# Is this function being used in any capacity?
def throw_alert():
    print("Please review webdriver status.")
    for _ in range(3):
        bell()
        sleep(0.1)
    input()


def repeat(function, times):
    for _ in range(times):
        function()


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)
    short_nap()


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()


def element_title_strip(element):
    return element.text.title().strip()


def scroll_to_top(browser):
    body_element = browser.find_element_by_tag_name("body")
    scroll_into_view(browser, body_element)


def get_element_attributes(browser, element):
    attributes = browser.execute_script(
        'var items = {};'
        'for (index = 0; index < arguments[0].attributes.length; ++index)'
        '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; '
        'return items;', element)
    pprint(attributes)


def four_character_padding(value):
    return value.zfill(4)


def eight_character_padding(value):
    return value.zfill(8)


def zipped_list(list1, list2):
    return list(zip(list1, list2))


def get_direct_children(element):
    return element.find_elements_by_xpath("./*")


def list_to_string(list):
    return "\n".join(list)


def newline_split(string):
    return string.split('\n')


def set_reception_number(document, reception_number):
    document.reception_number = reception_number


def set_description_link(document, link):
    document.description_link = link


def set_image_link(document, link):
    document.image_link = link


def get_direct_link(link):
    return link.get_attribute("href")


def date_from_string(string):
    try:
        format = '%m/%d/%Y'
        return datetime.strptime(string, format).strftime(format)
    except ValueError:
        return string


# def clear_search_field(handle_field_function):
#     while get_field_value(handle_field_function) != "":
#         handle_field_function.clear()


def enter_field_value(handle_field_function, value):
    try:
        handle_field_function.send_keys(Keys.UP + value)
    except StaleElementReferenceException:
        print(f'Encountered a StaleElementReferenceException trying to '
              f'enter "{value}" value into appropriate field, trying again...')


# def fill_search_field(handle_field_function, value):
#     while get_field_value(handle_field_function) != value:
#         enter_field_value(handle_field_function, value)


# Used for crocodile, performing the same function as "fill_search_field" but not as effectively
# please review
def enter_field_information(field, information):
    field.send_keys(information)


def print_list_by_index(list, web_element=None):
    if web_element is None:
        [print(list.index(element), element, '\n---------------\n') for element in list]
    else:
        [print(list.index(element), element.text, '\n---------------\n') for element in list]
