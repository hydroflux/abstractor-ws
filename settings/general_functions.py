from datetime import datetime
from pprint import pprint
from random import randint
from time import sleep

from settings.classes.counties import county_dictionary
from settings.settings import abstraction_type

# Timeout / Wait Variables
timeout = randint(20, 30)
long_timeout = randint(120, 180)
short_timeout = randint(5, 10)


def naptime():
    sleep(randint(3, 4))  # Consider adding an additional second if running into issues while using naps


def short_nap():
    sleep(randint(1, 2))


def medium_nap():
    sleep(randint(10, 20))


def long_nap():
    sleep(randint(30, 45))


def get_county_data(county_name):
    return county_dictionary.get(county_name)


def start_timer():
    return datetime.now()


def stop_timer(start_time):
    return datetime.now() - start_time


def report_execution_time(start_time):
    return str(stop_timer(start_time))


def handle_document_list_option(document_list):
    if document_list is not None:
        return f'{len(document_list)} documents imported for processing.'
    else:
        return ''


def start_program_timer(county, document_list=None):
    start_time = start_timer()
    print(f'{county} - {abstraction_type} started on: \n'
          f'{str(start_time.strftime("%B %d, %Y %H:%M:%S"))}\n\n'
          f'{handle_document_list_option(document_list)}')
    return start_time


def stop_program_timer(start_time):
    print(f'Total Run Time: {report_execution_time(start_time)}')


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)
    short_nap()


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()


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


def get_element_class(element):
    return element.get_attribute("class")


def check_active_class(element):
    if get_element_class(element).endswith("active"):
        return True


def get_parent_element(element):
    return element.find_element_by_xpath("..")


def four_character_padding(value):
    return value.zfill(4)


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
    return "/n".join(list)


def set_reception_number(document, reception_number):
    document.reception_number = reception_number


def set_document_link(document, link):
    document.link = link


def get_direct_link(document_link):
    return document_link.get_attribute("href")


def get_field_value(field):
    return field.get_attribute("value").strip()
