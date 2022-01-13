from settings.county_variables.jaguar import search_results_title, validation_class_name, invalid_search_message
from selenium_utilities.open import assert_window_title
from selenium_utilities.locators import locate_element_by_class_name


def validate_search(browser, document):
    if not assert_window_title(browser, search_results_title):
        print(f'Browser failed to successfully execute search for '
              f'"{document.extrapolate_value()}", validating search...')
        error_message_element = locate_element_by_class_name(browser, validation_class_name,
                                                             "search results", False, document)
        if error_message_element.text.strip() == invalid_search_message:
            print(invalid_search_message)
        else:
            print('Unable to identify the issue, please review.')
            print(error_message_element.text.strip())
        print('Please review and press enter to continue...')


def verify_results_loaded(browser, document):
    return True
