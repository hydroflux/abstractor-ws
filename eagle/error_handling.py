from selenium_utilities.locators import locate_element_by_class_name

from settings.general_functions import naptime, throw_alert

from eagle.eagle_variables import error_message_class, error_message_text


# def locate_error_message(browser):
#     try:
#         error_message_present = EC.presence_of_element_located((By.CLASS_NAME, error_message_class))
#         WebDriverWait(browser, timeout).until(error_message_present)
#         error_message = browser.find_element_by_class_name(error_message_class)
#         return error_message
#     except TimeoutException:
#         print("Browser timed out trying to locate error message after PDF failed to load, please review.")
#         # Refreshing fixed the issue; count = 1
#         throw_alert()


def check_for_error(browser, document):
    print(f'Checking for error during processing of {document.extrapolate_value()}...')
    error_message = locate_element_by_class_name(browser, error_message_class, "PDF error message", document=document)
    if type(error_message) is not None or error_message.text.startswith(error_message_text):
        print(f'An error occurred while opening the document located at '
              f'{document.extrapolate_value()}, refreshing the page to try again.')
        browser.refresh()
        naptime()
        return error_message_text
    else:
        print('No error appear to have occurred, please review.')
        throw_alert()
