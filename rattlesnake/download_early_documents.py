import os

from selenium.webdriver.support.ui import Select
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id as locate_element
from selenium_utilities.locators import locate_elements_by_tag_name
from selenium_utilities.open import assert_window_title, open_url

from settings.county_variables.rattlesnake import (early_document_image_title,
                                                   early_download_value,
                                                   early_search_title,
                                                   early_search_url,
                                                   other_book_type_value,
                                                   page_image_title,
                                                   patent_book_type_value,
                                                   patent_range,
                                                   result_link_tag_name,
                                                   results_tag_name)
from settings.download_management import update_download
from settings.file_management import create_document_directory, last_document
from settings.general_functions import (four_character_padding,
                                        get_direct_link,
                                        javascript_script_execution, naptime)
from project_management.user_prompts import clear_terminal

from rattlesnake.search import clear_search, handle_document_value_numbers


def select_book_type(browser, document):
    book_type_selector = Select(locate_element(browser, document.search_attributes["Book Type"],
                                "book type selector", True, document))
    if int(document.document_value()[0]) in patent_range:
        book_type_selector.select_by_value(patent_book_type_value)
    else:
        book_type_selector.select_by_value(other_book_type_value)


def search_early_document(browser, document):
    select_book_type(browser, document)  # Select Book Type
    handle_document_value_numbers(browser, document)  # Update Volume & Page Numbers
    click_button(browser, locate_element, document.button_attributes["Submit Button"],
                 "submit button", document)  # Execute Search


def check_results(browser, document):
    search_results = locate_element(browser, document.search_attributes["Results Table Id"],
                                    "search results", document=document)
    if search_results is not None:
        first_result = locate_elements_by_tag_name(search_results, results_tag_name, "first result", document=document)
        volume = int(document.document_value()[0])
        if volume in patent_range and volume * 10 == int(first_result[2].text):
            return True
        elif volume == int(first_result[2].text):
            return True


def open_result(browser, document):
    search_results = locate_element(browser, document.search_attributes["Results Table Id"],
                                    "search results", document=document)
    result_script = get_direct_link(locate_elements_by_tag_name(
                    search_results, result_link_tag_name, "result link", True, document)[1])
    javascript_script_execution(browser, result_script)


def document_image_page_user_prompt():
    print('It appears that you are not on the document image page, would you like to '
          'try again, or continue to the next document?')
    input_selection = ('What would you like to do? \n'
                       '[1] Try Again \n'
                       '[2] Next Document \n')
    user_input = input(input_selection)
    while user_input.lower() not in ["1", "2", "y", "n", "yes", "no"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    print()
    return True if user_input.lower() in ["1", "y", "yes"] else False


def check_document_image_page(browser):
    input('Please press enter after opening early document volume...')
    if not assert_window_title(browser, early_document_image_title):
        return document_image_page_user_prompt()
    else:
        return True


def go_to_page(browser, document, page_value):
    page_selector = Select(locate_element(browser, document.search_attributes["Page Selector Id"],
                           "page selector", True, document))
    page_selector.select_by_value(str(page_value))


def download_page_prompt():
    print('Would you like to download this document page?')
    input_selection = ('[1] Yes \n'
                       '[2] No \n')
    user_input = input(input_selection)
    while user_input.lower() not in ["1", "2", "y", "n", "yes", "no"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    print()
    return True if user_input.lower() in ["1", "y", "yes"] else False


def set_early_document_download_name(document, count):
    value = document.document_value()
    document.download_value = early_download_value
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
    page_image = locate_element(browser, document.search_attributes["Page Image Id"], "page image", document=document)
    page_source = page_image.get_attribute('src')
    open_url(browser, page_source, page_image_title, "page image", document)


def download_page(browser, document, document_directory, count):
    number_files = len(os.listdir(document_directory))
    open_download_page(browser, document)
    browser.execute_script('window.print();')
    naptime()
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
                       '[2] No \n')
    user_input = input(input_selection)
    while user_input.lower() not in ["1", "2", "y", "n", "yes", "no"]:
        print(f'You entered "{user_input}" Please enter 1 or 2:')
        user_input = input(input_selection)
    return True if user_input.lower() in ["1", "y", "yes"] else False


def download_early_document_image(browser, document, document_directory, count=0, next_page=True):
    page_value = int(document.document_value()[1]) - 1
    go_to_page(browser, document, page_value)
    while next_page is True:
        if download_page_prompt():
            os.chdir(document_directory)
            set_early_document_download_name(document, count)
            download_page(browser, document, document_directory, count)
            count += 1
            page_value += 1
            # if next_page_prompt():
            click_button(browser, locate_element, document.button_attributes["Next Button"], "next page button", document)
        else:
            next_page = False


def handle_search_results(browser, document, document_directory):
    if check_results(browser, document):
        open_result(browser, document)
        download_early_document_image(browser, document, document_directory)
    else:
        print('Unable to locate correct search result on first try, please locate and open the correct Volume.')
        if check_document_image_page(browser):
            download_early_document_image(browser, document, document_directory)


def handle_document_search(browser, document_list, document, document_directory):
    volume = document.document_value()[0]
    if volume == last_document(document_list, document).document_value()[0] and len(document_list) > 1:
        download_early_document_image(browser, document, document_directory)
    else:
        open_url(browser, early_search_url, early_search_title, "old document search")
        clear_search(browser, document)
        search_early_document(browser, document)
        handle_search_results(browser, document, document_directory)


def download_early_documents(browser, target_directory, document_list):
    document_directory = create_document_directory(target_directory)
    for document in document_list:
        clear_terminal()
        print(f'Now searching {document.extrapolate_value()}...')
        handle_document_search(browser, document_list, document, document_directory)
