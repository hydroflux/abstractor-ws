from buffalo.frame_handling import switch_to_header_frame
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from buffalo.buffalo_variables import header_text_tag


def locate_header_text(browser):
    try:
        header_text_element_present = EC.presence_of_element_located((By.TAG_NAME, header_text_tag))
        WebDriverWait(browser, timeout).until(header_text_element_present)
        header_text_element = browser.find_element_by_tag_name(header_text_tag)
        return header_text_element
    except TimeoutException:
        print('Browser timed out trying to located header text during header validation, please review.')


def header_validation(browser, validation_text):
    switch_to_header_frame(browser)
    header_text_element = locate_header_text(browser).text
    return header_text_element.startswith(validation_text)


def page_is_loaded(browser, validation_text):
    if not header_validation(browser, validation_text):
        print(f'Browser indicates that it has not properly loaded '
              f'"{validation_text}", please review webdriver before continuing...')
        input()
    else:
        return True
