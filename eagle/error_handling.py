from selenium_utilities.locators import locate_element_by_class_name

from settings.general_functions import naptime

from settings.county_variables.eagle import error_message_class, error_message_text


def check_for_error(browser, document, alt=None):
    error_message = locate_element_by_class_name(browser, error_message_class, "search error message",
                                                 document=document, quick=True)
    if error_message is not None:
        print(f'Located an error during processing of {document.extrapolate_value()}...')
        print('error_message', error_message)
        print('error_message_text', error_message.text)
        if error_message.text.startswith(error_message_text):
            print(f'An error occurred while handling document located at '
                  f'{document.extrapolate_value()}, refreshing the page to try again.')
            browser.refresh()
            naptime()
            return error_message_text
        else:
            print('Unable to determine how to handle error, please review and press enter to continue...')
            input()
    elif alt == 'search':
        return False
    else:
        print('No error appears to have occurred, please review and press enter to continue...')
        input()
