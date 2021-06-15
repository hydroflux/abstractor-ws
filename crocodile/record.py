from settings.bad_search import no_document_image
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.export_settings import not_applicable
from settings.file_management import extrapolate_document_value, multiple_documents_comment
from settings.general_functions import (get_direct_children, get_element_text,
                                        list_to_string, set_image_link,
                                        set_reception_number, short_nap,
                                        timeout, title_strip, zipped_list)

from crocodile.crocodile_variables import (additional_legal_pages_class,
                                           bad_document_types,
                                           general_information_id, grantee_id,
                                           grantor_id, inactive, legal_id,
                                           link_tag,
                                           related_documents_buttons_class,
                                           related_documents_id, row_data_tag,
                                           row_header_tag, row_titles,
                                           show_all_rows_text, table_body_tag,
                                           table_row_tag)


def locate_general_information(document_information, document):
    try:
        general_information_present = EC.presence_of_element_located((By.ID, general_information_id))
        WebDriverWait(document_information, timeout).until(general_information_present)
        general_information = document_information.find_element_by_id(general_information_id)
        return general_information
    except TimeoutException:
        print(f'Browser timed out trying to locate general information for '
              f'{extrapolate_document_value(document)}')


def locate_document_table(browser, document, table_id, type):
    try:
        document_table_present = EC.presence_of_element_located((By.ID, table_id))
        WebDriverWait(browser, timeout).until(document_table_present)
        document_table = browser.find_element_by_id(table_id)
        return document_table
    except TimeoutException:
        print(f'Browser timed out trying to locate {type} document table for '
              f'{extrapolate_document_value(document)}, please review.')


# Stripped straight from leopard
def get_table_rows(browser, document_table, document):
    try:
        table_rows_present = EC.presence_of_element_located((By.TAG_NAME, table_row_tag))
        WebDriverWait(browser, timeout).until(table_rows_present)
        table_rows = document_table.find_elements_by_tag_name(table_row_tag)
        return table_rows
    except TimeoutException:
        print(f'Browser timed out getting table rows for '
              f'{extrapolate_document_value(document)}.')


# This could be a generalized function
def get_row_data(row, tag):
    return row.find_elements_by_tag_name(tag)


def get_general_information_data(browser, general_information_table, document):
    general_information_rows = get_table_rows(browser, general_information_table, document)
    headers = get_row_data(general_information_rows[0], row_header_tag)
    data = get_row_data(general_information_rows[1], row_data_tag)
    return zipped_list(headers, data)


# Copied & audited from leopard
def check_list_elements(general_information, title_options):
    print(1)
    for header, data in general_information:
        print(2)
        if get_element_text(header) in title_options:
            print(3)
            if get_element_text(header) in row_titles["document_image"]:
                print(4)
                return data
            if get_element_text(data) != "":
                print(5)
                return get_element_text(data)
            else:
                print(6)
                return not_applicable
    return 'No row title match found.'


def check_document_image_availability(general_information, document):
    document_image = check_list_elements(general_information, row_titles["document_image"])
    document_image_link = document_image.find_element_by_tag_name(link_tag)
    if document_image_link.get_attribute(inactive) == "true":
        return None
    else:
        image_link = document_image_link.get_attribute("href")
        set_image_link(document, image_link)


def record_reception_number(general_information, dictionary, document):
    reception_number = check_list_elements(general_information, row_titles["reception_number"])
    set_reception_number(document, reception_number)
    dictionary["Reception Number"].append(reception_number)


def record_book_and_page(general_information, dictionary):
    book_and_page = check_list_elements(general_information, row_titles["book_and_page"])
    if book_and_page == not_applicable:
        dictionary["Book"].append(book_and_page)
        dictionary["Page"].append(book_and_page)
    else:
        book, page = book_and_page.replace("/", "").split()
        if book == "0":
            dictionary["Book"].append(not_applicable)
        else:
            dictionary["Book"].append(book)
        if page == "0":
            dictionary["Page"].append(not_applicable)
        else:
            dictionary["Page"].append(page)


def record_document_type(general_information, dictionary):
    document_type = check_list_elements(general_information, row_titles["document_type"])
    if document_type == not_applicable or document_type in bad_document_types:
        document_type = check_list_elements(general_information, row_titles["alt_document_type"])
    dictionary["Document Type"].append(title_strip(document_type))


def record_recording_date(general_information, dictionary):
    recording_date = check_list_elements(general_information, row_titles["recording_date"])
    dictionary["Recording Date"].append(recording_date[:10])


def get_number_legal_pages(legal_table):
    try:
        legal_pages = legal_table.find_element_by_class_name(additional_legal_pages_class).text
        return int(legal_pages[(legal_pages.rfind(" ") + 1):])
    except NoSuchElementException:
        return 1


def get_legal_table(browser):
    try:
        legal_table = browser.find_element_by_id(legal_id)
        return legal_table
    except NoSuchElementException:
        return False


def drop_last_line(string):
    return string[:string.rfind("\n")]


def locate_legal_buttons_row(legal_table, document):
    try:
        legal_buttons_present = EC.element_to_be_clickable((By.CLASS_NAME, additional_legal_pages_class))
        WebDriverWait(legal_table, timeout).until(legal_buttons_present)
        legal_buttons_row = legal_table.find_element_by_class_name(additional_legal_pages_class)
        return legal_buttons_row
    except TimeoutException:
        print(f'Browser timed out trying to access legal table row containing page buttons for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_legal_table_buttons(legal_buttons_row, document):
    try:
        legal_table_buttons_present = EC.element_to_be_clickable((By.TAG_NAME, link_tag))
        WebDriverWait(legal_buttons_row, timeout).until(legal_table_buttons_present)
        legal_table_buttons = legal_buttons_row.find_elements_by_tag_name(link_tag)
        return legal_table_buttons
    except TimeoutException:
        print(f'Browser timed out trying to access supplemental legal data for '
              f'{extrapolate_document_value(document)}, please review.')


def next_legal_table(legal_table, document, current_page):
    legal_buttons_row = locate_legal_buttons_row(legal_table, document)
    legal_table_buttons = locate_legal_table_buttons(legal_buttons_row, document)
    for button in legal_table_buttons:
        if int(button.text) == current_page:
            button.click()
            short_nap()
            return


def multi_page_legal(browser, legal_table, document, number_pages):
    legal_data = drop_last_line(title_strip(join_column_without_title(legal_table)))
    for current_page in range(number_pages - 1):
        next_legal_table(legal_table, document, (current_page + 2))
        legal_table = get_legal_table(browser)
        legal_data = f'{legal_data}\n{drop_last_line(title_strip(join_column_without_title(legal_table)))}'
        print(legal_data)


def handle_legal_tables(browser, legal_table, document):
    number_pages = get_number_legal_pages(legal_table)
    if number_pages == 1:
        return title_strip(join_column_without_title(legal_table))
    else:
        return multi_page_legal(browser, legal_table, document, number_pages)


def check_for_additional_legal(browser, dictionary, document):
    legal_table = get_legal_table(browser)
    if legal_table:
        return handle_legal_tables(browser, legal_table, document)


def record_legal_information(browser, general_information, dictionary, document):
    legal = check_list_elements(general_information, row_titles["legal"])
    additional_legal = check_for_additional_legal(browser, dictionary, document)
    if not additional_legal:
        if legal == not_applicable or legal in bad_document_types:
            dictionary["Legal"].append("")
        else:
            dictionary["Legal"].append(legal)
    else:
        if legal == not_applicable or legal in bad_document_types:
            dictionary["Legal"].append(additional_legal)
        else:
            dictionary["Legal"].append(f'{legal}\n{additional_legal}')


def record_general_information(browser, dictionary, document):
    general_information_table = locate_document_table(browser, document, general_information_id, "general information")
    general_information = get_general_information_data(browser, general_information_table, document)
    check_document_image_availability(general_information, document)
    record_reception_number(general_information, dictionary, document)
    record_book_and_page(general_information, dictionary)
    record_document_type(general_information, dictionary)
    record_recording_date(general_information, dictionary)
    record_legal_information(browser, general_information, dictionary, document)


def join_column_without_title(string):
    return '\n'.join(string.text.split('\n')[1:])


def drop_hyphen(text):
    if text.startswith("-"):
        return text[1:]
    else:
        return text


def record_grantor_information(browser, dictionary, document):
    grantor_table = locate_document_table(browser, document, grantor_id, "grantor")
    grantor = title_strip(join_column_without_title(grantor_table))
    dictionary["Grantor"].append(drop_hyphen(grantor))
    print("grantor", grantor)


def record_grantee_information(browser, dictionary, document):
    grantee_table = locate_document_table(browser, document, grantee_id, "grantee")
    grantee = title_strip(join_column_without_title(grantee_table))
    dictionary["Grantee"].append(drop_hyphen(grantee))
    print("grantee", grantee)


def get_related_documents_table(browser):
    try:
        related_documents_table = browser.find_element_by_id(related_documents_id)
        return related_documents_table
    except NoSuchElementException:
        return False


def locate_related_documents_buttons(browser, document):
    try:
        related_documents_buttons_present = EC.presence_of_element_located(
            (By.CLASS_NAME, related_documents_buttons_class))
        WebDriverWait(browser, timeout).until(related_documents_buttons_present)
        related_documents_buttons = browser.find_element_by_class_name(related_documents_buttons_class)
        return related_documents_buttons
    except TimeoutException:
        print(f'Browser timed out trying to locate related documents buttons for '
              f'{extrapolate_document_value(document)}, please review.')


def expand_all_rows(browser, buttons):
    for button in buttons:
        if button.text == show_all_rows_text:
            button.click()
            return


def display_all_related_documents(browser, document):
    related_documents_buttons = locate_related_documents_buttons(browser, document)
    buttons = related_documents_buttons.find_elements_by_tag_name(link_tag)
    expand_all_rows(browser, buttons)


def get_related_documents_rows(related_documents_table):
    related_documents_sub_tables = related_documents_table.find_elements_by_tag_name(table_body_tag)
    related_documents_data = related_documents_sub_tables[4]
    return get_direct_children(related_documents_data)


# def locate_related_row_data(browser, row):
#     try:

#     except StaleElementReferenceException:
#         scroll_into_view(browser, row)


def get_related_row_data(row):
    try:
        row_fields = get_direct_children(row)
        related_document = f'{title_strip(row_fields[4].text)} {title_strip(row_fields[3].text)} {(row_fields[8].text)}'
        print("related_document", related_document)
        return related_document
    except StaleElementReferenceException:
        print("Encountered a stale element reference exception, trying again")
        return None


def aggregate_related_row_data(browser, related_documents_list, row):
    row_data = get_related_row_data(row)
    if row_data is None:
        print("row", row)
        row_data = get_related_row_data(row)
    related_documents_list.append(row_data)


def handle_related_documents_table(browser, related_documents_table, document):
    related_documents_rows = get_related_documents_rows(related_documents_table)
    related_documents_list = []
    # for row in related_documents_rows:
    #     print(related_documents_rows.index(row), row)
    #     # get_related_row_data(row)
    for row in related_documents_rows:
        print(related_documents_rows.index(row), row.text)
        aggregate_related_row_data(browser, related_documents_list, row)
    return list_to_string(related_documents_list)


def record_related_document_information(browser, dictionary, document):
    related_documents_table = get_related_documents_table(browser)
    if not related_documents_table:
        dictionary["Related Documents"].append("")
    else:
        # display_all_related_documents(browser, document)  # Run a few tests once in production to see if  necessary
        related_documents = handle_related_documents_table(browser, related_documents_table, document)
        print("related_documents", related_documents)
        dictionary["Related Documents"].append(related_documents)


def record_comments(county, dictionary, document):
    if document.number_results > 1:
        dictionary["Comments"].append(multiple_documents_comment(county, document))
    else:
        dictionary["Comments"].append("")
    if document.image_link is None:
        no_document_image(dictionary, document)
    # This is bad practice, no document image checks against the last comment


def record_document(browser, county, dictionary, document):
    # If document_number == N/A, return book & page???
    record_general_information(browser, dictionary, document)
    record_grantor_information(browser, dictionary, document)
    record_grantee_information(browser, dictionary, document)
    record_related_document_information(browser, dictionary, document)
    record_comments(county, dictionary, document)
