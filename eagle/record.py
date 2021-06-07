from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import search_errors
from settings.file_management import (check_length, drop_last_entry,
                                      extrapolate_document_value)
from settings.general_functions import (long_timeout, medium_nap, naptime,
                                        scroll_into_view, scroll_to_top,
                                        short_nap, timeout,
                                        update_sentence_case_extras)

from eagle.eagle_variables import (document_information_id,
                                   document_table_class, error_message_text,
                                   image_container_id, index_table_tags,
                                   information_links_class, less_info,
                                   loading_status, missing_values, more_info,
                                   no_image_text, pdf_viewer_load_id,
                                   related_table_class, result_button_tag,
                                   result_buttons_class)
from eagle.error_handling import check_for_error, no_image_comment

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("record", __name__)


def access_image_container(browser):
    try:
        image_container_present = EC.presence_of_element_located((By.ID, image_container_id))
        WebDriverWait(browser, timeout).until(image_container_present)
        image_container = browser.find_element_by_id(image_container_id)
        return image_container
    except TimeoutException:
        print("Browser timed out waiting for image container to load.")


def document_image_exists(browser):
    image_container = access_image_container(browser)
    if image_container.text == no_image_text:
        return False
    else:
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
    while pdf_load_status(browser, document).startswith(loading_status) or pdf_load_status == error_message_text:
        short_nap()  # using short_nap in order to try & grab all related documents
        # Consider changing to even naptime ~~~ originally 0.5 second sleep
        # Updating sleep time would be more efficient here because it would force a nap only
        # If the  PDF hasn't loaded properly


def handle_document_image_status(browser, document):
    if document_image_exists(browser):
        wait_for_pdf_to_load(browser, document)
        naptime()  # Remove after running successful 'review' test
        #  medium_nap()  # Use for review
        # Overall this is a bad practice because it's adding 1 - 2 seconds for a
        # 0.1% chance it misses (based on testing)
    else:
        medium_nap()


def get_document_information(browser, document):
    try:
        document_information_present = EC.presence_of_element_located((By.ID, document_information_id))
        WebDriverWait(browser, timeout).until(document_information_present)
        document_information = browser.find_element_by_id(document_information_id)
        return document_information
    except TimeoutException:
        print(f'Browser timed out while trying to get document information for '
              f'{extrapolate_document_value(document)}.')


def access_document_information_tables(browser, document, document_information):
    try:
        document_tables_present = EC.presence_of_element_located((By.CLASS_NAME, document_table_class))
        WebDriverWait(browser, timeout).until(document_tables_present)
        document_tables = document_information.find_elements_by_class_name(document_table_class)
        return document_tables
    except TimeoutException:
        print(f'Browser timed out while trying to access document table information for '
              f'{extrapolate_document_value(document)}.')


def get_informational_links(browser, document, document_information):
    try:
        informational_links_present = EC.presence_of_element_located((By.CLASS_NAME, information_links_class))
        WebDriverWait(browser, timeout).until(informational_links_present)
        informational_links = document_information.find_elements_by_class_name(information_links_class)
        return informational_links
    except TimeoutException:
        print(f'Browser timed out while trying to get informational links for {extrapolate_document_value(document)}.')


def open_informational_grandparent(browser, link):
    grandparent = link.find_element_by_xpath("../..")
    scroll_into_view(browser, grandparent)
    short_nap()  # Using for testing -- does not work consistently
    link.click()


def open_by_link_text(browser):  # this doesn't work
    try:
        more_info_text_present = EC.element_to_be_clickable((By.LINK_TEXT, more_info))
        WebDriverWait(browser, timeout).until(more_info_text_present)
        more_info_text = browser.find_element_by_link_text(more_info)
        more_info_text.click()
    except TimeoutException:
        print("Browser timed out while trying to show more info using link text, please review.")


def open_informational_link(browser, link):  # needs to be updated to work on a smaller screen
    try:
        scroll_into_view(browser, link)
        short_nap()  # Using for testing -- does not work consistently
        link.click()
    except ElementClickInterceptedException:
        try:
            open_informational_grandparent(browser, link)
        except ElementClickInterceptedException:
            open_by_link_text(browser)  # this doesn't work, need to try something else


def review_and_open_links(browser, links):
    for link in links:
        if link.text == more_info:
            open_informational_link(browser, link)


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


def record_indexing_data(document_table, dataframe):
    reception_field, recording_date = access_indexing_information(document_table)
    reception_number, book, page = split_reception_field(reception_field)
    dataframe["Reception Number"].append(reception_number)
    dataframe["Book"].append(book)
    dataframe["Page"].append(page)
    dataframe["Recording Date"].append(recording_date[:10])
    return reception_number


def record_name_data(document_table, dataframe):
    grantor, grantee = access_indexing_information(document_table)
    dataframe["Grantor"].append(drop_superfluous_information(grantor))
    dataframe["Grantee"].append(drop_superfluous_information(grantee))


def record_legal_data(document_table, dataframe):
    table_rows = access_table_rows(document_table)
    legal_data = table_rows[1].find_elements_by_tag_name(index_table_tags[2])
    if legal_data == []:
        dataframe["Legal"].append(search_errors[2])
    else:
        legal = legal_data[-1].text
        if legal.endswith(search_errors[4]):
            legal = legal[:-11]  # Might make more sense to make this a .strip with -10 rather than -11
        dataframe["Legal"].append(legal)


def record_related_documents(document_table, dataframe):
    related_table_rows = document_table.find_elements_by_class_name(related_table_class)
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
            notes = f'Notes: {notes}'
            if dataframe["Legal"][-1] == "":
                dataframe["Legal"][-1] = notes
            else:
                dataframe["Legal"][-1] = f'{dataframe["Legal"][-1]}\n{notes}'
    except IndexError:
        pass


def aggregate_document_information(document_tables, dataframe):
    reception_number = record_indexing_data(document_tables[1], dataframe)
    record_document_type(document_tables[0], dataframe)
    record_name_data(document_tables[2], dataframe)
    record_legal_data(document_tables[4], dataframe)
    record_related_documents(document_tables[-2], dataframe)
    record_notes(document_tables, dataframe)
    return reception_number


def record_comments(county, dataframe, document, image_available):
    if document.number_results > 1:
        dataframe["Comments"].append(f'Multiple documents located at {extrapolate_document_value(document)}'
                                     f' on the {county} recording website; Each of the {document.number_results}'
                                     f' documents has been listed, please review')
    else:
        dataframe["Comments"].append("")
    if not image_available:
        if dataframe["Comments"][-1] == "":
            dataframe["Comments"][-1] == no_image_comment(document)
        else:
            dataframe["Comments"][-1] = f'{dataframe["Comments"][-1]}; {no_image_comment(document)}'


def record_document_fields(browser, county, dataframe, document, image_available):
    document_information = get_document_information(browser, document)
    document_tables = access_document_information_tables(browser, document, document_information)
    display_all_information(browser, document)
    reception_number = aggregate_document_information(document_tables, dataframe)
    record_comments(county, dataframe, document, image_available)
    scroll_to_top(browser)
    return reception_number


def review_entry(browser, county, dataframe, document, image_available):
    while dataframe["Grantor"][-1] == missing_values[0] and dataframe["Grantee"][-1] == missing_values[0]\
            and dataframe["Related Documents"][-1] == missing_values[1]:
        print("Recording of last document was processed incorrectly, attempting to record again.")
        re_record_document_fields(browser, county, dataframe, document, image_available)


def re_record_document_fields(browser, county, dataframe, document, image_available):
    drop_last_entry(dataframe)
    record_document_fields(browser, county, dataframe, document, image_available)


def get_result_buttons(browser, document):
    try:
        result_buttons_present = EC.presence_of_element_located((By.CLASS_NAME, result_buttons_class))
        WebDriverWait(browser, timeout).until(result_buttons_present)
        result_buttons = browser.find_element_by_class_name(result_buttons_class)
        return result_buttons
    except TimeoutException:
        print(f'Browser timed out while trying to locate result buttons for {extrapolate_document_value(document)}.')


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
    except ElementClickInterceptedException:
        print("Button click intercepted while trying to view previous / next result, trying again")
        naptime()
        button.click()
    except StaleElementReferenceException:
        print("Stale element reference exception encountered while trying to view previous / next result, trying again")
        naptime()
        button.click()


def next_result(browser, document):
    next_result_button = get_next_result_button(browser, document)
    click_result_button(browser, next_result_button)


def get_reception_number(browser, document):
    wait_for_pdf_to_load(browser, document)
    document_information = get_document_information(browser, document)
    document_tables = access_document_information_tables(browser, document, document_information)
    reception_field, recording_date = access_indexing_information(document_tables[1])
    return split_reception_field(reception_field)[0]


def record_document(browser, county, dataframe, document):
    image_available = handle_document_image_status(browser, document)
    document_number = record_document_fields(browser, county, dataframe, document, image_available)
    check_length(dataframe)
    review_entry(browser, county, dataframe, document, image_available)
    return document_number
