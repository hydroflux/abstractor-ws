from datetime import datetime
from pprint import pprint
from random import randint
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.keys import Keys

from settings.classes.counties import county_dictionary
from settings.settings import abstraction_type

# Timeout / Wait Variables
timeout = randint(20, 30)
long_timeout = randint(120, 180)
short_timeout = randint(5, 10)


def naptime():
    sleep(randint(3, 4))  # Consider adding an additional second if running into issues while using naps


def micro_nap():
    if randint(0, 1) == 0:
        sleep(0.25)
    else:
        sleep(0.5)


def short_nap():
    sleep(randint(1, 2))


def medium_nap():
    sleep(randint(10, 20))


def long_nap():
    sleep(randint(30, 45))


def get_county_data(county_name):
    return county_dictionary.get(county_name.lower())


def start_timer():
    return datetime.now()


def bell():
    print("\a")


def stop_timer(start_time):
    return datetime.now() - start_time


def report_execution_time(start_time):
    return str(stop_timer(start_time))


def throw_alert():
    print("Please review webdriver status.")
    for _ in range(3):
        bell()
        sleep(0.1)
    input()


def repeat(function, times):
    for _ in range(times):
        function()


def handle_document_list_option(document_list):
    if document_list is not None:
        return f'\n{len(document_list)} documents imported for processing.'
    else:
        return ''


def start_program_timer(county, document_list=None):
    start_time = start_timer()
    print(f'{county} - {abstraction_type} started on: \n'
          f'{str(start_time.strftime("%B %d, %Y %H:%M:%S"))}'
          f'{handle_document_list_option(document_list)}')
    return start_time


def stop_program_timer(start_time):
    print(f'Total Run Time: {report_execution_time(start_time)}')


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def center_element(browser, element):
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = browser.execute_script('return window.innerHeight')
    window_y = browser.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y
    browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def javascript_script_execution(browser, script):
    browser.execute_script(script)
    short_nap()


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()


def element_title_strip(element):
    return element.text.title().strip()


def update_sentence_case_extras(text):
    return (text.replace("'S ", "'s ")
            .replace("1St ", "1st ")
            .replace("2Nd ", "2nd ")
            .replace("3Rd ", "3rd ")
            .replace("4Th ", "4th "))


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


def get_element_onclick(element):
    return element.get_attribute("onclick")


def get_element_class(element):
    return element.get_attribute("class")


def check_active_class(element):
    if get_element_class(element).endswith("active"):
        return True


def get_parent_element(element):
    return element.find_element_by_xpath("..")


def four_character_padding(value):
    return value.zfill(4)


def eight_character_padding(value):
    return value.zfill(8)


def update_number_results(document, total_results):
    document.number_results = int(total_results)


def assert_window_title(browser, window_title):
    try:
        assert window_title in browser.title.strip()
        return True
    except AssertionError:
        return False


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


def get_direct_link(document_link):
    return document_link.get_attribute("href")


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
        return [print(list.index(element), element, '\n---------------\n') for element in list]
    else:
        return [print(list.index(element), element.text, '\n---------------\n') for element in list]
