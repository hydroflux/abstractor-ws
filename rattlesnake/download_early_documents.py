from settings.user_prompts import clear_terminal
from selenium_utilities.inputs import click_button
from rattlesnake.search import clear_search, handle_document_value_numbers
from selenium_utilities.open import assert_window_title, open_url
from selenium_utilities.locators import locate_element_by_id as locate_input

from rattlesnake.rattlesnake_variables import early_search_url, early_search_title, early_document_image_title


def search_early_document(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_input, document.input_ids["Volume"],
                 "Volume Input", document)
    click_button(browser, locate_input, document.button_ids["Submit Button"],
                 "submit button", document)  # Execute Search


def handle_document_image_page_user_input():
    print('It appears that you are not on the document image page, would you like to '
          'try again, or continue to the next document?')
    input_selection = ('What would you like to do? \n'
                       '[1] Try Again \n'
                       '[2] Next Document')
    user_input = input(input_selection)
    while user_input not in ["1", "2"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    return True if user_input == "1" else False


def check_document_image_page(browser):
    clear_terminal()
    input('Please press enter after opening early document volume...')
    if not assert_window_title(browser, early_document_image_title):
        return handle_document_image_page_user_input()


def download_early_documents(browser, target_directory, document_list):
    for document in document_list:
        print(f'Now searching {document.document_value()}...')
        open_url(browser, early_search_url, early_search_title, "old document search")
        clear_search(browser, document)
        search_early_document(browser, document)
        if check_document_image_page(browser):
            pass
