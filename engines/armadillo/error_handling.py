from selenium_utilities.locators import locate_element_by_class_name

from project_management.timers import naptime


def check_for_error(browser, abstract, document, alt=None):
    error_message = locate_element_by_class_name(browser, abstract.county.classes["Error Message"],
                                                 "search error message", document=document, quick=True)
    if error_message is not None:
        print(f'Located an error during processing of {document.extrapolate_value()}...')
        if error_message.text.startswith(abstract.county.messages["Error Message"]):
            print(f'An error occurred while handling document located at '
                  f'{document.extrapolate_value()}, refreshing the page to try again.')
            browser.refresh()
            naptime()
            return abstract.county.messages["Error Message"]
        else:
            print('Unable to determine how to handle error, please review and press enter to continue...')
            input()
            return abstract.county.messages["Error Message"]
    elif alt == 'search':
        return False
    else:
        print('No error appears to have occurred, please review and press enter to continue...')
        input()
        return abstract.county.messages["Error Message"]