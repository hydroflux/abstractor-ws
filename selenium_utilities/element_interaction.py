from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout


def center_element(browser, element):
    try:
        desired_y = (element.size['height'] / 2) + element.location['y']
        window_h = browser.execute_script('return window.innerHeight')
        window_y = browser.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    except StaleElementReferenceException:
        print('Browser encountered a StaleElementReferenceException while trying to center '
              'element, please review and press enter to continue...')
        input()


def get_element_onclick(element):
    return element.get_attribute("onclick")


def get_element_class(element):
    return element.get_attribute("class")


# def check_active_class(element):
#     if get_element_class(element).endswith("active"):
#         return True


def is_active_class(element):
    element_class = element.get_attribute("class")
    if element_class.endswith("active"):
        return True


def get_parent_element(element):
    return element.find_element("xpath", "..")


# move out of 'general_functions' & update dependencies
def get_element_text(element):
    return element.text


def access_title_case_text(data):
    # added .strip() when updating buffalo -- may negatively impact eagle
    return data.text.strip().title()


def handle_alert(browser):
    try:
        alert_present = EC.alert_is_present()
        WebDriverWait(browser, timeout).until(alert_present)
        alert = browser.switch_to.alert
        alert.accept()
        return True
    except TimeoutException:
        print("Browser timed out while attempting to locate an alert, please review.")
