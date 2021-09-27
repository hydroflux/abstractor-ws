import os

from selenium.webdriver.support.ui import Select

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id as locate_element
from selenium_utilities.open import assert_window_title, open_url

from settings.download_management import update_download
from settings.file_management import create_document_directory
from settings.general_functions import four_character_padding
from settings.user_prompts import clear_terminal

from rattlesnake.rattlesnake_variables import (early_document_image_title,
                                               early_search_title,
                                               early_search_url, page_image_id,
                                               page_image_title,
                                               page_selector_id)
from rattlesnake.search import clear_search, handle_document_value_numbers


def search_early_document(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_element, document.input_ids["Volume"],
                 "Volume Input", document)
    click_button(browser, locate_element, document.button_ids["Submit Button"],
                 "submit button", document)  # Execute Search


def document_image_page_user_prompt():
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
        return document_image_page_user_prompt()
    else:
        return True


def go_to_page(browser, document, page_value):
    page_selector = Select(locate_element(browser, page_selector_id, "page selector", True, document))
    page_selector.selectByValue(page_value)


def download_page_prompt():
    print('Would you like to download this document page?')
    input_selection = ('[1] Yes \n'
                       '[2] No')
    user_input = input(input_selection)
    while user_input not in ["1", "2"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    return True if user_input == "1" else False


def set_early_document_download_name(document, count):
    value = document.document_value()
    if count == 0:
        document.new_name = (f'{document.county.prefix}-'
                             f'{four_character_padding(value[0])}-'
                             f'{four_character_padding(value[1])}.pdf')
    else:
        document.new_name = (f'{document.county.prefix}-'
                             f'{four_character_padding(value[0])}-'
                             f'{four_character_padding(value[1])}-'
                             f'{count}.pdf')


def open_download_page(browser, document):
    page_image = locate_element(browser, page_image_id, "page image", document=document)
    page_source = page_image.get_attribute('src')
    open_url(browser, page_source, page_image_title, "page image", document)


def download_page(browser, document, document_directory, count):
    number_files = len(os.listdir(document_directory))
    open_download_page(browser, document)
    browser.execute_script('window.print();')
    if update_download(browser, document_directory, document, number_files):
        print(f'Successfully downloaded page {count + 1} for '
              f'{document.extrapolate_value()}.')
        browser.back()
    else:
        print('Browser failed to downloaded page {count + 1} for '
              f'{document.document_value()}, please review.')
        input()


def next_page_prompt():
    print('Would you like to go to the next page?')
    input_selection = ('[1] Yes \n'
                       '[2] No')
    user_input = input(input_selection)
    while user_input not in ["1", "2"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    return True if user_input == "1" else False


def download_early_document_image(browser, document, document_directory, count=0, next_page=True):
    page_value = int(document.document_value()[1] - 1)
    while next_page is True:
        go_to_page(browser, document, page_value)
        if download_page_prompt():
            set_early_document_download_name(document, count)
            download_page(browser, document, document_directory, count)
            count += 1
            page_value = page_value + count
            next_page = next_page_prompt()
        else:
            next_page = False


def download_early_documents(browser, target_directory, document_list):
    document_directory = create_document_directory(target_directory)
    for document in document_list:
        clear_terminal()
        print(f'Now searching {document.extrapolate_value()}...')
        open_url(browser, early_search_url, early_search_title, "old document search")
        clear_search(browser, document)
        search_early_document(browser, document)
        if check_document_image_page(browser):
            download_early_document_image(browser, document, document_directory)
