from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.element_interaction import center_element

from settings.bad_search import no_document_image
from settings.county_variables.eagle import (document_information_id,
                                             document_table_class,
                                             error_message_text,
                                             image_container_id,
                                             index_table_tags,
                                             information_links_class,
                                             less_info, loading_status,
                                             login_error_text, missing_values,
                                             more_info, no_image_text,
                                             pdf_viewer_load_id,
                                             related_table_class,
                                             result_button_tag,
                                             result_buttons_class)
from settings.export_settings import search_errors
from settings.file_management import (check_last_document, check_length,
                                      drop_last_entry,
                                      multiple_documents_comment)
from settings.general_functions import (long_timeout, medium_nap, naptime,
                                        scroll_to_top, short_nap, timeout,
                                        update_sentence_case_extras)
from settings.settings import execution_review

from eagle.error_handling import check_for_error

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)


def access_image_container_text(browser, document):
    try:
        image_container_present = EC.presence_of_element_located((By.ID, image_container_id))
        WebDriverWait(browser, timeout).until(image_container_present)
        image_container = browser.find_element_by_id(image_container_id)
        return image_container.text
    except TimeoutException:
        print('Browser timed out waiting for image container to load for '
              f'{document.extrapolate_value()}, please review.')
        return check_for_error(browser, document)


def get_image_container(browser, document):
    image_container_text = access_image_container_text(browser, document)
    while image_container_text == error_message_text or image_container_text is None:
        image_container_text = access_image_container_text(browser, document)
    return image_container_text


def document_image_exists(browser, document):
    image_container_text = get_image_container(browser, document)
    print(image_container_text)
    if image_container_text == no_image_text or image_container_text == login_error_text:
        return False
    else:
        print('image_container_text', image_container_text)
        return True


def pdf_load_status(browser, document):
    try:
        pdf_viewer_loaded = EC.presence_of_element_located((By.ID, pdf_viewer_load_id))
        WebDriverWait(browser, long_timeout).until(pdf_viewer_loaded)
        load_status = browser.find_element_by_id(pdf_viewer_load_id).text
        return load_status
    except TimeoutException:
        print("Browser timed out while waiting for the PDF Viewer to load, checking for error.")
        return check_for_error(browser, document)


def wait_for_pdf_to_load(browser, document):
    while pdf_load_status(browser, document).startswith(loading_status) or \
            pdf_load_status(browser, document) == error_message_text:
        medium_nap()
        # Status Quo (below) as of 06/23/21 changing to try & work with related documents issue
        # short_nap()  # using short_nap in order to try & grab all related documents
        # Consider changing to even naptime ~~~ originally 0.5 second sleep
        # Updating sleep time would be more efficient here because it would force a nap only
        # If the  PDF hasn't loaded properly


def handle_document_image_status(browser, document):
    if document_image_exists(browser, document):
        wait_for_pdf_to_load(browser, document)
        # naptime()   # Part of test 2 & test 3
        return True
    else:
        print(f'No document image exists for '
              f'{document.extrapolate_value()}, please review.')
        medium_nap()
        return False


def get_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_id(document_information_id)
        return document_information
    except TimeoutException:
        print(f'Browser timed out while trying to get document information for '
              f'{document.extrapolate_value()}.')


def access_document_information_tables(browser, document, document_information):
    try:
        document_tables_present = EC.presence_of_element_located((By.CLASS_NAME, document_table_class))
        WebDriverWait(browser, timeout).until(document_tables_present)
        document_tables = document_information.find_elements_by_class_name(document_table_class)
        return document_tables
    except TimeoutException:
        print(f'Browser timed out while trying to access document table information for '
              f'{document.extrapolate_value()}.')


def get_informational_links(browser, document, document_information):
    try:
        informational_links_present = EC.presence_of_element_located((By.CLASS_NAME, information_links_class))
        WebDriverWait(browser, timeout).until(informational_links_present)
        informational_links = document_information.find_elements_by_class_name(information_links_class)
        return informational_links
    except TimeoutException:
        print(f'Browser timed out while trying to get informational links for {document.extrapolate_value()}.')


# def open_informational_grandparent(browser, link):
#     grandparent = link.find_element_by_xpath("../..")
#     scroll_into_view(browser, grandparent)
#     short_nap()  # Using for testing -- does not work consistently
#     link.click()


def open_informational_link(browser, link):  # needs to be updated to work on a smaller screen
    center_element(browser, link)
    link.click()


def handle_information_links(browser, link):
    try:
        while link.text == more_info:
            open_informational_link(browser, link)
            short_nap()
    except StaleElementReferenceException:
        print('Encountered StaleElementReferenceException '
              'while handling information links, please review.')
        input()


def review_and_open_links(browser, links):
    for link in links:
        handle_information_links(browser, link)


def display_all_information(browser, document):
    document_information = get_document_information(browser, document)
    information_links = get_informational_links(browser, document, document_information)
    review_and_open_links(browser, information_links)


def drop_superfluous_information(string):
    if string.endswith(less_info):
        return string[:-(len(less_info) + 1)]
    else:
        return string


def access_table_body(document_table):
    return document_table.find_element_by_tag_name(index_table_tags[0])


def access_table_rows(table_body):
    body_text = table_body.find_elements_by_tag_name(index_table_tags[1])
    return body_text


def access_title_case_text(data):
    return update_sentence_case_extras(data.text.title())


def access_field_body_no_title(field_info):
    return "\n".join(field_info.text.split("\n")[1:])


def access_field_body(field_info):
    return "\n".join(field_info.text.split("\n")[1:]).title()


def access_indexing_information(document_table):
    table_body = access_table_body(document_table)
    table_rows = access_table_rows(table_body)
    return map(access_field_body, table_rows)


def record_document_type(document_table, dataframe):
    document_type = update_sentence_case_extras(document_table.text.title())
    dataframe["Document Type"].append(document_type)


def split_reception_field(reception_field):
    if "Book" in reception_field and "Page" in reception_field:
        reception_fields = reception_field.split("\n")
        reception_number = reception_fields[0]
        book = reception_fields[2]
        page = reception_fields[4]
    else:
        reception_number = reception_field
        book = search_errors[2]
        page = search_errors[2]
    return reception_number, book, page


def record_indexing_data(document_table, dataframe, document):
    reception_field, recording_date = access_indexing_information(document_table)
    reception_number, book, page = split_reception_field(reception_field)
    document.reception_number = reception_number
    dataframe["Reception Number"].append(reception_number)
    dataframe["Book"].append(book)
    dataframe["Page"].append(page)
    dataframe["Recording Date"].append(recording_date[:10])


def record_name_data(document_table, dataframe):
    grantor, grantee = access_indexing_information(document_table)
    dataframe["Grantor"].append(update_sentence_case_extras(drop_superfluous_information(grantor)))
    dataframe["Grantee"].append(update_sentence_case_extras(drop_superfluous_information(grantee)))


def record_legal_data(document_table, dataframe):
    table_rows = access_table_rows(document_table)
    legal_data = table_rows[1].find_elements_by_tag_name(index_table_tags[2])
    if legal_data == []:
        dataframe["Legal"].append(search_errors[2])
    else:
        legal = legal_data[-1].text
        if legal.endswith(search_errors[4]):
            legal = legal.strip()  # Running along with test 1
        dataframe["Legal"].append(drop_superfluous_information(legal))


def locate_related_documents_table_rows(document, document_table):
    try:
        related_table_rows = document_table.find_elements_by_class_name(related_table_class)
        return related_table_rows
    except StaleElementReferenceException:
        print(f'Browser encountered StaleElementReferenceException trying to '
              f'located related documents table rows for '
              f'{document.extrapolate_value()}, trying again.')
        return False


def get_related_documents_table_rows(browser, document_table, document):
    center_element(browser, document_table)
    related_documents_table_rows = locate_related_documents_table_rows(document, document_table)
    while related_documents_table_rows is False:
        print(f'Unable to locate the "Related Documents Table" rows for '
              f'{document.extrapolate_value()}, trying again...')
        naptime()
        related_documents_table_rows = locate_related_documents_table_rows(document, document_table)
    return related_documents_table_rows


def record_related_documents(browser, document_table, dataframe, document):
    # If none then ... ? conditional -- need to test with some print statements to see general feedback first
    related_table_rows = get_related_documents_table_rows(browser, document_table, document)
    related_documents_info = list(map(access_table_body, related_table_rows))
    related_document_list = list(map(access_title_case_text, related_documents_info))
    related_documents = "\n".join(related_document_list)
    dataframe["Related Documents"].append(drop_superfluous_information(related_documents))


def record_notes(document_tables, dataframe):
    try:
        notes = access_field_body_no_title(document_tables[5])
        if notes == search_errors[3] or notes == search_errors[4] or notes == search_errors[5]:
            pass
        elif notes.startswith(search_errors[3]) or notes.endswith(search_errors[3]):
            pass
        else:
            if notes.strip() != "":
                notes = f'Notes: {notes}'
                if dataframe["Legal"][-1] == "":
                    dataframe["Legal"][-1] = notes
                else:
                    dataframe["Legal"][-1] = f'{dataframe["Legal"][-1]}\n{notes}'
    except IndexError:
        pass


def aggregate_document_information(browser, document_tables, dataframe, document):
    record_indexing_data(document_tables[1], dataframe, document)
    record_document_type(document_tables[0], dataframe)
    record_name_data(document_tables[2], dataframe)
    record_legal_data(document_tables[4], dataframe)
    record_related_documents(browser, document_tables[-2], dataframe, document)
    record_notes(document_tables, dataframe)


def record_effective_date(dataframe):
    dataframe['Effective Date'].append('')


def record_volume(dataframe):
    dataframe['Volume'].append('')


def record_document_link(dataframe):
    dataframe["Document Link"].append('')


def record_comments(dataframe, document, image_available):
    if document.number_results == 1:
        dataframe["Comments"].append("")
    elif document.number_results > 1:
        dataframe["Comments"].append(multiple_documents_comment(document))
    if not image_available:
        no_document_image(dataframe, document)


def access_document_tables(browser, document):
    document_information = get_document_information(browser, document)
    return access_document_information_tables(browser, document, document_information)


def record_document_fields(browser, dataframe, document, image_available):
    document_tables = access_document_tables(browser, document)
    if execution_review:
        medium_nap()   # Adding a flag instead of having to comment the line our every time for review
        # should probably be it's own function if continue using in this manner
    display_all_information(browser, document)
    aggregate_document_information(browser, document_tables, dataframe, document)
    record_effective_date(dataframe)
    record_volume(dataframe)
    record_document_link(dataframe)
    record_comments(dataframe, document, image_available)
    scroll_to_top(browser)


def review_entry(browser, dataframe, document, image_available):
    while dataframe["Grantor"][-1] == missing_values[0] and dataframe["Grantee"][-1] == missing_values[0]\
            and dataframe["Related Documents"][-1] == missing_values[1] or document.reception_number.strip() == '':
        print("Recording of last document was processed incorrectly, attempting to record again.")
        re_record_document_fields(browser, dataframe, document, image_available)


def re_record_document_fields(browser, dataframe, document, image_available):
    drop_last_entry(dataframe)
    browser.refresh()
    medium_nap()
    record_document_fields(browser, dataframe, document, image_available)


def get_result_buttons(browser, document):
    try:
        result_buttons_present = EC.presence_of_element_located((By.CLASS_NAME, result_buttons_class))
        WebDriverWait(browser, timeout).until(result_buttons_present)
        result_buttons = browser.find_element_by_class_name(result_buttons_class)
        return result_buttons
    except TimeoutException:
        print(f'Browser timed out while trying to locate result buttons for {document.extrapolate_value()}.')


def get_previous_result_button(browser, document):
    result_buttons = get_result_buttons(browser, document)
    return result_buttons.find_elements_by_tag_name(result_button_tag)[0]


def previous_result(browser, document):
    previous_result_button = get_previous_result_button(browser, document)
    scroll_to_top(browser)
    previous_result_button.click()
    naptime()


def get_next_result_button(browser, document):
    result_buttons = get_result_buttons(browser, document)
    return result_buttons.find_elements_by_tag_name(result_button_tag)[1]


def click_result_button(browser, button):
    try:
        scroll_to_top(browser)
        button.click()
        short_nap()  # Nap is necessary, consider lengthening if app breaks at this point
        return True
    except ElementClickInterceptedException:
        print("Button click intercepted while trying to view previous / next result, trying again")
        # naptime()
        # button.click()
    except StaleElementReferenceException:
        print("Stale element reference exception encountered while trying to view previous / next result, trying again")
        # naptime()
        # button.click()


def handle_click_next_result_button(browser, document, button):
    while not click_result_button(browser, button):
        naptime()
        button = get_next_result_button(browser, document)


def next_result(browser, document):
    next_result_button = get_next_result_button(browser, document)
    handle_click_next_result_button(browser, document, next_result_button)
    naptime()  # DO NOT REMOVE NAP -- slow server speeds can cause duplicate recordings of the same document


# def get_reception_number(browser, document):
#     wait_for_pdf_to_load(browser, document)
#     document_information = get_document_information(browser, document)
#     document_tables = access_document_information_tables(browser, document, document_information)
#     reception_field, _ = access_indexing_information(document_tables[1])
#     document.reception_number = split_reception_field(reception_field)[0]


def access_download_information(browser, dataframe, document):
    image_available = handle_document_image_status(browser, document)
    if not image_available:
        no_document_image(dataframe, document)
    else:
        document_tables = access_document_tables(browser, document)
        reception_field, _ = access_indexing_information(document_tables[1])
        reception_number, _, _ = split_reception_field(reception_field)
        document.reception_number = reception_number


def build_document_download_information(browser, dataframe, document):
    reception_number = access_download_information(browser, dataframe, document)
    while document.reception_number.strip() == '':
        print('Browser did not correctly access reception number for '
              f'{document.extrapolate_value()}, trying again...')
        naptime()
        reception_number = access_download_information(browser, dataframe, document)
    dataframe['Reception Number'].append(reception_number)
    dataframe['Comments'].append('')


def record(browser, document_list, dataframe, document):
    image_available = handle_document_image_status(browser, document)
    record_document_fields(browser, dataframe, document, image_available)
    check_length(dataframe)
    check_last_document(dataframe, document_list, document)
    review_entry(browser, dataframe, document, image_available)
