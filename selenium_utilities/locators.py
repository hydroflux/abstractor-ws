# Standard Library Import(s)
import logging  # Used to log messages to the console
from typing import List, Optional, Union  # List for specifying a type hint for a list, Optional for indicating a variable can be None

# Selenium Module(s)
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver  # Used to interact with the browser
from selenium.webdriver.remote.webelement import WebElement  # Used to interact with the elements on a web page
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select # Used to select options from dropdown menus
from selenium.webdriver.support.wait import WebDriverWait

# Local Module(s)
from project_management.timers import timeout, micro_timeout

# Global variable mapping from string identifiers to Selenium's 'By' locator types
# LOCATOR_TYPE_MAPPING = {
#     'id': By.ID,
#     'xpath': By.XPATH,
#     'link_text': By.LINK_TEXT,
#     'partial_link_text': By.PARTIAL_LINK_TEXT,
#     'name': By.NAME,
#     'tag_name': By.TAG_NAME,
#     'class_name': By.CLASS_NAME,
#     'css_selector': By.CSS_SELECTOR
# }


# def locate_element_need_to_update(locator: Union[WebDriver, WebElement], attr: str, locator_type: str, locator_value: str, clickable: bool = False, timeout: int = 30) -> WebElement:
#     """
#     Locates an element on the page using the given locator.

#     Args:
#         locator (Union[WebDriver, WebElement]): The WebDriver or WebElement instance to use for locating the element.
#         attr (str): The attribute of the element to locate.
#         locator_type (str): The type of the locator (e.g., 'xpath', 'id', 'class_name').
#         locator_value (str): The value of the locator.
#         clickable (bool, optional): Whether the element should be clickable. Defaults to False.
#         timeout (int, optional): The number of seconds to wait for the element to appear. Defaults to 30.

#     Returns:
#         WebElement: The WebElement object representing the located element.

#     Raises:
#         NoSuchElementException: If the element is not found.
#         TimeoutException: If the element is not found within the given timeout.
#         StaleElementReferenceException: If the reference to the element becomes stale before the function can complete.
#     """
#     try:
#         # logging.info(f"Locating element '{attr}' with {locator_type.upper()}: '{locator_value}'")
#         if clickable:
#             element_present = EC.element_to_be_clickable((LOCATOR_TYPE_MAPPING[locator_type], locator_value))
#         else:
#             element_present = EC.presence_of_element_located((LOCATOR_TYPE_MAPPING[locator_type], locator_value))
        
#         WebDriverWait(locator, timeout).until(element_present)
#         element = locator.find_element(LOCATOR_TYPE_MAPPING[locator_type], locator_value)
#         # logging.info(f"Successfully located element '{attr}' with {locator_type.upper()}: '{locator_value}'")
#         return element
#     except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
#         handle_exception(e, attr, locator_type, locator_value)


def locate_element_by_class_name(locator, class_name, type, clickable=False, document=None, quick=False):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            else:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element("class name", class_name)
        return element
    except TimeoutException:
        return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def locate_elements_by_class_name(locator, class_name, type, clickable=False, document=None,
                                  quick=False, alternate=None, timeout=timeout):
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            else:
                elements_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements("class name", class_name)
        return elements
    except TimeoutException:
        if alternate is not None:
            try:
                if clickable:
                    elements_present = EC.element_to_be_clickable((By.CLASS_NAME, alternate))
                else:
                    elements_present = EC.presence_of_element_located((By.CLASS_NAME, alternate))
                WebDriverWait(locator, timeout).until(elements_present)
                elements = locator.find_elements("class name", alternate)
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
        element = locator.find_element("id", id)
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
        element = locator.find_element("name", name)
        return element
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)


def locate_element_by_tag_name(locator, tag_name, type, clickable=False, document=None, quick=False, timeout=timeout):
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.TAG_NAME, tag_name))
            else:
                element_present = EC.presence_of_element_located((By.TAG_NAME, tag_name))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element("tag name", tag_name)
        return element
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except StaleElementReferenceException:
        print(f'StaleElementReferenceException experienced trying to located "{type}", returning NONE...')


def locate_elements_by_tag_name(locator, tag_name, type, clickable=False, document=None, quick=False, timeout=timeout):
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.TAG_NAME, tag_name))
            else:
                elements_present = EC.presence_of_element_located((By.TAG_NAME, tag_name))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements("tag name", tag_name)
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
        element = locator.find_element("xpath", xpath)
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
        elements = locator.find_elements("xpath", xpath)
        return elements
    except TimeoutException:
        if not quick:
            return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)
        

def locate_element_by_css_selector(locator: Union[WebDriver, WebElement], css_selector: str, type: str, clickable: bool = False, document: Optional[dict] = None, quick: bool = False) -> Optional[WebElement]:
    """
    Locate an element by CSS selector.

    Args:
        locator (Union[WebDriver, WebElement]): The WebDriver or WebElement instance to use for locating the element.
        css_selector (str): The CSS selector of the element to locate.
        type (str): The type of the element (for logging purposes).
        clickable (bool, optional): Whether the element should be clickable. Defaults to False.
        document (Optional[dict], optional): The document information (for logging purposes). Defaults to None.
        quick (bool, optional): Whether to perform a quick search without waiting. Defaults to False.

    Returns:
        Optional[WebElement]: The located WebElement, or None if not found.
    """
    try:
        if not quick:
            if clickable:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            else:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            WebDriverWait(locator, timeout).until(element_present)
        element = locator.find_element(By.CSS_SELECTOR, css_selector)
        return element
    except TimeoutException:
        return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)
    except StaleElementReferenceException:
        print(f'StaleElementReferenceException experienced trying to locate "{type}", returning NONE...')
        return None
        

def locate_elements_by_css_selector(locator: Union[WebDriver, WebElement], css_selector: str, type: str, clickable: bool = False, document: Optional[dict] = None, quick: bool = False) -> Optional[List[WebElement]]:
    """
    Locate multiple elements by CSS selector.

    Args:
        locator (Union[WebDriver, WebElement]): The WebDriver or WebElement instance to use for locating the elements.
        css_selector (str): The CSS selector of the elements to locate.
        type (str): The type of the elements (for logging purposes).
        clickable (bool, optional): Whether the elements should be clickable. Defaults to False.
        document (Optional[dict], optional): The document information (for logging purposes). Defaults to None.
        quick (bool, optional): Whether to perform a quick search without waiting. Defaults to False.

    Returns:
        Optional[List[WebElement]]: The list of located WebElements, or None if not found.
    """
    try:
        if not quick:
            if clickable:
                elements_present = EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            else:
                elements_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
            WebDriverWait(locator, timeout).until(elements_present)
        elements = locator.find_elements(By.CSS_SELECTOR, css_selector)
        return elements
    except TimeoutException:
        return print_timeout_statement(type, document)
    except NoSuchElementException:
        if not quick:
            return print_no_such_element_statement(type, document)
    except StaleElementReferenceException:
        print(f'StaleElementReferenceException experienced trying to locate "{type}", returning NONE...')
        return None


def get_element_value(element: WebElement) -> str:
    """
    Returns the value of a given element.

    Args:
        element (WebElement): The element to get the value from.

    Returns:
        str: The value of the element.
    """
    # logging.info("Getting element value...")
    attribute = element.get_attribute("value")
    if attribute is not None:
        # logging.info("Element value retrieved successfully.")
        return attribute.strip()
    else:
        # logging.info(f"""Element "{element}" has no value attribute, returning text.""")
        return element.text


def select_dropdown_option_by_value(locator: WebDriver, attr: str, locator_type: str, locator_value: str, value: str) -> None:
    """
    Selects a dropdown option by value and verifies that the value is correctly selected.

    Args:
        locator (WebDriver): The WebDriver instance to use for selecting the dropdown option.
        attr (str): The attribute of the dropdown.
        locator_type (str): The locator type of the dropdown (e.g., 'xpath', 'id', 'class_name').
        locator_value (str): The locator value of the dropdown.
        value (str): The value of the option to select.

    Raises:
        NoSuchElementException: If the dropdown is not found.
        TimeoutException: If the dropdown is not found within the given timeout.
        StaleElementReferenceException: If the reference to the dropdown becomes stale before the function can complete.
        ValueError: If the selected value is not correctly set in the dropdown.
    """
    # logging.info(f"Attempting to select dropdown option '{attr}' with {locator_type.upper()}: '{locator_value}' by value '{value}'")
    try:
        dropdown_element = locate_element(locator, attr, locator_type, locator_value, clickable=True)
        dropdown = Select(dropdown_element)
        dropdown.select_by_value(value)
        # logging.info(f"Dropdown option '{attr}' with {locator_type.upper()}: '{locator_value}' selected successfully.")

        # Verify that the value is correctly selected
        selected_value = get_element_value(dropdown_element)
        if selected_value != value:
            raise ValueError(f"Failed to select the correct value '{value}' in dropdown '{attr}' with {locator_type.upper()}: '{locator_value}'. Selected value is '{selected_value}'.")

        # logging.info(f"Verified that the dropdown option '{attr}' with {locator_type.upper()}: '{locator_value}' has the correct value '{value}' selected.")
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
        handle_exception(e, attr, locator_type, locator_value)
    except ValueError as e:
        logging.error(e)
        raise


def print_timeout_statement(type, document):
    if document is None:
        print(f'Browser timed out trying to locate "{type}", please review.')
    else:
        print(f'Browser timed out trying to locate "{type}" for '
              f'{document.extrapolate_value()}, please review.')
    return False


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


def generate_error_message(e: Exception, attr: str = "", locator_type: str = "", locator_value: str = "", button_name: str = "") -> str:
    """
    Generates an error message based on the exception type.

    Args:
        e (Exception): The exception that was raised.
        attr (str, optional): The attribute of the element. Defaults to "".
        locator_type (str, optional): The type of the locator. Defaults to "".
        locator_value (str, optional): The value of the locator. Defaults to "".
        button_name (str, optional): The name of the button. Defaults to "".

    Returns:
        str: The generated error message.
    """
    if isinstance(e, NoSuchElementException):
        return f'Browser unable to locate any element(s) "{attr}" with {locator_type.upper()}: "{locator_value}"'
    elif isinstance(e, TimeoutException):
        return f'Timed out trying to locate element(s) "{attr}" with {locator_type.upper()}: "{locator_value}"'
    elif isinstance(e, ElementClickInterceptedException):
        if button_name:
            return f'Element click intercepted while trying to click the "{button_name}". Please review.'
        else:
            return f'Element click intercepted while trying to click "{attr}" with {locator_type.upper()}: "{locator_value}". Please review.'
    elif isinstance(e, StaleElementReferenceException):
        if locator_type and attr:
            return f'Browser encountered a StaleElementReferenceException while trying to locate "{attr}" with {locator_type.upper()}: "{locator_value}".'
        else:
            return 'Browser encountered a StaleElementReferenceException while trying to center element.'
    elif isinstance(e, ValueError):
        return f'ValueError: {str(e)}'
    else:
        return f'An unexpected exception occurred: {str(e)}'


def handle_exception(e: Exception, attr: str = "", locator_type: str = "", locator_value: str = "", button_name: str = "") -> None:
    """
    Handles exceptions by logging appropriate messages based on the exception type and prints the message to the console.

    Args:
        e (Exception): The exception that was raised.
        attr (str, optional): The attribute of the element. Defaults to "".
        locator_type (str, optional): The type of the locator. Defaults to "".
        locator_value (str, optional): The value of the locator. Defaults to "".
        button_name (str, optional): The name of the button. Defaults to "".
    """
    msg = generate_error_message(e, attr, locator_type, locator_value, button_name)
    # logging.error(msg)
    print(msg)
    
    if isinstance(e, NoSuchElementException):
        raise NoSuchElementException(msg) from None
    elif isinstance(e, TimeoutException):
        raise TimeoutException(msg) from None
    elif isinstance(e, ElementClickInterceptedException):
        raise ElementClickInterceptedException(msg) from None
    elif isinstance(e, StaleElementReferenceException):
        raise StaleElementReferenceException(msg) from None
    elif isinstance(e, ValueError):
        raise ValueError(msg) from None
    else:
        raise e
