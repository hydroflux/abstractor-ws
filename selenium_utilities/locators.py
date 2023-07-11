from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout, micro_timeout


def locate_element_by_class_name(locator, class_name, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            else:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_class_name(class_name)
        return element
    except TimeoutException:
        return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def locate_elements_by_class_name(locator, class_name, type, clickable=False, document=None,
                                  quick=False, alternate=None):
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            else:
                elements_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements_by_class_name(class_name)
        return elements
    except TimeoutException:
        if alternate is not None:
            try:
                if clickable:
                    elements_present = EC.element_to_be_clickable((By.CLASS_NAME, alternate))
                else:
                    elements_present = EC.presence_of_element_located((By.CLASS_NAME, alternate))
                WebDriverWait(locator, timeout).until(elements_present)
                elements = locator.find_elements_by_class_name(alternate)
                return elements
            except TimeoutException:
                if not quick:
                    return print_timeout_statement(type, document)
        else:
            print("1000")
            if not quick:
                return print_timeout_statement(type, document)


def locate_element_by_id(locator, id, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.ID, id))
            else:
                element_present = EC.presence_of_element_located((By.ID, id))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_id(id)
        return element
    except TimeoutException:
        return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)
    except StaleElementReferenceException:
        print(f'StaleElementReferenceException experienced trying to located "{type}", returning NONE...')


def locate_element_by_name(locator, name, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.NAME, name))
            else:
                element_present = EC.presence_of_element_located((By.NAME, name))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_name(name)
        return element
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def locate_element_by_tag_name(locator, tag_name, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.TAG_NAME, tag_name))
            else:
                element_present = EC.presence_of_element_located((By.TAG_NAME, tag_name))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_tag_name(tag_name)
        return element
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except StaleElementReferenceException:
        print(f'StaleElementReferenceException experienced trying to located "{type}", returning NONE...')


def locate_elements_by_tag_name(locator, tag_name, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.TAG_NAME, tag_name))
            else:
                elements_present = EC.presence_of_element_located((By.TAG_NAME, tag_name))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements_by_tag_name(tag_name)
        return elements
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)


def locate_element_by_xpath(locator, xpath, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.XPATH, xpath))
            else:
                element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element_by_xpath(xpath)
        return element
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def locate_elements_by_xpath(locator, xpath, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.XPATH, xpath))
            else:
                elements_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements_by_xpath(xpath)
        return elements
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def print_timeout_statement(type, document):
    if document is None:
        print(f'Browser timed out trying to locate "{type}", please review.')
    else:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')
    # return False


def print_no_such_element_statement(type, document):
    if document is None:
        print(f'Browser unable to locate any element "{type}", please review.')
    else:
        print(f'Browser unable to locate any element "{type}" for '
              f'{document.extrapolate_value()}, please review.')
    # return False


# Fix ordering of document & clickable arguments & parameters across all functions
def locate_element(locator, attribute_type, attribute, attribute_descriptor, clickable=False, document=None,
                   quick=False, alternate=None):
    if attribute_type == "id":
        return locate_element_by_id(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "class":
        return locate_element_by_class_name(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "classes":
        return locate_elements_by_class_name(locator, attribute, attribute_descriptor, clickable, document, quick, alternate)
    elif attribute_type == "name":
        return locate_element_by_name(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "tag":
        return locate_element_by_tag_name(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "tags":
        return locate_elements_by_tag_name(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "xpath":
        return locate_element_by_xpath(locator, attribute, attribute_descriptor, clickable, document, quick)
    elif attribute_type == "tags":
        return locate_element_by_xpath(locator, attribute, attribute_descriptor, clickable, document, quick)


# ELEMENT IS VISIBLE
def element_visible_by_id(locator, id):
    try:
        element_visible = EC.visibility_of_element_located((By.ID, id))
        WebDriverWait(locator, micro_timeout).until(element_visible)
        return True
    except TimeoutException:
        return False
