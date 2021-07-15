from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from buffalo.buffalo_variables import main_frame_name


def locate_iframe_by_name(browser, iframe_name):
    try:
        iframe_present = EC.presence_of_element_located((By.NAME, iframe_name))
        WebDriverWait(browser, timeout).until(iframe_present)
        iframe = browser.find_element_by_name(iframe_name)
        return iframe
    except TimeoutException:
        print(f'Browser timed out trying to locate {iframe_name}, please review.')


def switch_to_default_content(browser):
    browser.switch_to.default_content()


def switch_to_main_frame(browser):
    switch_to_default_content(browser)
    main_frame = locate_iframe_by_name(browser, main_frame_name)
    browser.switch_to.frame(main_frame)
