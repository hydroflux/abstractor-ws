from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
from engines.eagle.open_document import get_search_results, retry_execute_search, wait_for_results
from engines.eagle.error_handling import check_for_error
from engines.eagle.login import check_login_status
from engines.eagle.open_document import (retry_search,
                                         validate_search)
from engines.eagle.search import clear_search
from project_management.timers import naptime
from selenium_utilities.element_interaction import center_element
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url


def enter_name_value(browser, abstract, document):
    enter_input_value(browser, locate_input, abstract.county.inputs["Start Date"],
                      "start date input", abstract.start_date, document)
    enter_input_value(browser, locate_input, abstract.county.inputs["End Date"],
                      "end date input", abstract.end_date, document)
    enter_input_value(browser, locate_input, abstract.county.inputs["Name"],
                      "name input", abstract.search_name, document)


def execute_search(browser, abstract, document):
    enter_name_value(browser, abstract, document)
    click_button(browser, locate_input, abstract.county.buttons["Submit Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_url(browser, abstract.county.urls["Search Page"],
             abstract.county.titles["Search Page"], "document search page")
    check_login_status(browser, abstract)
    if not check_for_error(browser, abstract, document, 'search'):
        clear_search(browser, abstract, document)
        naptime()  # Consider testing without this nap to see if necessary
        execute_search(browser, abstract, document)


def count_name_results(browser, abstract, document):
    result_rows = get_search_results(browser, abstract, document)
    if result_rows is not False:
        return int(browser.find_element("xpath", '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/ul/li[1]/div[2]').text.split(' ')[-3])


def handle_name_result_count(browser, abstract, document):
    search_status = wait_for_results(browser, abstract)
    if search_status == abstract.county.messages["Failed Search"]:
        print(f'Initial search failed, attempting to execute search again for '
              f'{document.extrapolate_value()}')
        search_status = retry_execute_search(browser, abstract, document, search_status)
    if search_status == abstract.county.messages["No Results"]:
        print(f'No results located at {document.extrapolate_value()}, please review.')
    else:
        return count_name_results(browser, abstract, document)


def check_name_search_results(browser, abstract, document):
    result_count = handle_name_result_count(browser, abstract, document)
    if result_count:
        return result_count


def record_indexing_data(abstract, row_text):
    reception_number, document_type, recording_date = row_text[0].split('•')
    abstract.dataframe['Reception Number'].append(reception_number.strip())
    abstract.dataframe['Document Type'].append(document_type.strip().title())
    abstract.dataframe['Recording Date'].append(recording_date.strip()[:10])
    return row_text[1:]


def record_grantor(abstract, row_text):
    if row_text[1].startswith('Grantee'):
        abstract.dataframe['Grantor'].append('No Record Found')
        return row_text[1:]
    else:
        abstract.dataframe['Grantor'].append(row_text[1].title())
        return row_text[2:]


def record_grantee(abstract, row_text):
    if row_text[1].startswith('Legal'):
        abstract.dataframe['Grantee'].append('No Record Found')
        return row_text[1:]
    else:
        abstract.dataframe['Grantee'].append(row_text[1].title())
        return row_text[2:]


def record_legal(abstract, row_text):
    if row_text[1].startswith('Notes'):
        abstract.dataframe['Legal'].append('Not Available in Search Results')
        return row_text[1:]
    else:
        abstract.dataframe['Legal'].append(row_text[1].title())
        return row_text[2:]


def record_everything_else(abstract):
    abstract.dataframe["Book"].append('')
    abstract.dataframe["Volume"].append('')
    abstract.dataframe["Page"].append('')
    abstract.dataframe["Document Link"].append('')
    abstract.dataframe["Effective Date"].append('')
    abstract.dataframe["Related Documents"].append('')
    abstract.dataframe["Comments"].append('')


def record_name_result_row(browser, abstract, document, row):
    row_text = row.text.split('\n')
    if len(row_text[0]) == 1:
        row_text = row_text[1:]
    # print('             ', row_text)
    row_text = record_indexing_data(abstract, row_text)
    # print('             ', row_text)
    row_text = record_grantor(abstract, row_text)
    # print('             ', row_text)
    row_text = record_grantee(abstract, row_text)
    # print('             ', row_text)
    row_text = record_legal(abstract, row_text)
    # print('             ', row_text)
    record_everything_else(abstract)


def record_result_page(browser, abstract, document):
    result_rows = get_search_results(browser, abstract, document)
    for row in result_rows:
        print(row.text)
        row_info = get_search_results(browser, abstract, document)[result_rows.index(row)]
        record_name_result_row(browser, abstract, document, row_info)


# def record_result_page(browser, abstract, document):
#     result_rows = get_search_results(browser, abstract, document)
#     for row in result_rows:
#         center_element(browser, row)
#         row.click()
#         sleep(0.5)
#         while get_search_results(browser, abstract, document)[result_rows.index(row)].text.split('\n')[1:][-2] == 'Loading Related Documents...':
#             sleep(0.5)
#         row_info = get_search_results(browser, abstract, document)[result_rows.index(row)]
#         record_name_result_row(browser, abstract, document, row_info)


def next_search_results_page(browser, abstract, document):
    # A better idea would be to check the recorded results vs. the result count
    try:
        next_button = browser.find_element("link text", 'Next')
        center_element(browser, next_button)
        next_button.click()
        sleep(10)
    except NoSuchElementException:
        print("No more pages!")
        print(f'Recorded {len(abstract.dataframe["Grantor"])} during processing.')
        return
    except ElementClickInterceptedException:
        print("No more pages!")
        print(f'Recorded {len(abstract.dataframe["Grantor"])} during processing.')
        return


def record_search_names(browser, abstract, document, result_count):
    while len(abstract.dataframe['Grantor']) < result_count:
        record_result_page(browser, abstract, document)
        next_search_results_page(browser, abstract, document)
        abstract.check_length()


def handle_name_search_results(browser, abstract, document):
    while not validate_search(browser, abstract, document):
        retry_search(browser, abstract, document)
    result_count = check_name_search_results(browser, abstract, document)
    print(f'Located {str(result_count)} results to be processed:')
    if result_count:
        record_search_names(browser, abstract, document, result_count)
    else:
        print(f'No results returned for "{abstract.search_name}", please adjust your search parameters.')


def name_search(browser, abstract):
    #
    #  BAD PRACTICE / FIX FUNCTIONS
    #
    document = ''
    #
    #
    #
    search(browser, abstract, document)
    handle_name_search_results(browser, abstract, document)
    # record results
