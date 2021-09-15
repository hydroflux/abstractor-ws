from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import timeout


def locate_search_field_by_id(browser, document, id, type):
    try:
        search_field_present = EC.element_to_be_clickable((By.ID, id))
        WebDriverWait(browser, timeout).until(search_field_present)
        search_field = browser.find_element_by_id(id)
        return search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate "{type}" field for '
              f'{document.extrapolate_value()}.')
