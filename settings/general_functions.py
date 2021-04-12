from random import randint
from time import sleep

from settings.classes.counties import county_dictionary


def naptime():
    # sleep(randint(3, 6))
    sleep(randint(2, 3))


def short_nap():
    sleep(randint(1, 2))


def long_nap():
    sleep(randint(30, 45))


def get_county_data(county):
    return county_dictionary.get(county)


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()
