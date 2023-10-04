from functools import partial
from selenium.common.exceptions import StaleElementReferenceException
from engines.armadillo.disclaimer import check_for_disclaimer

from selenium_utilities.element_interaction import access_title_case_text, center_element
from selenium_utilities.locators import (locate_element_by_id, locate_element_by_tag_name,
                                         locate_elements_by_class_name)

from project_management.timers import medium_nap, naptime

from serializers.recorder import (record_comments, record_empty_values,
                                  record_value)

from settings.county_variables.general import search_errors
from settings.general_functions import (scroll_to_top,
                                        short_nap)
from settings.invalid import no_document_image
from settings.county_variables.general import execution_review

from engines.armadillo.error_handling import check_for_error


def access_image_container(browser, abstract, document):
    image_container = locate_element_by_id(browser, abstract.county.ids["Image Container"],
                                           "image container", False, document)
    while image_container is None:
        check_for_error(browser, abstract, document)
        image_container = locate_element_by_id(browser, abstract.county.ids["Image Container"],
                                               "image container", False, document)
    return image_container.text


def access_pdf_load_status(browser, abstract, document):
    loading_status_element = locate_element_by_id(browser, abstract.county.ids["PDF Viewer Load Marker"],
                                                  "PDF Viewer load status", False, document)
    while loading_status_element is None:
        check_for_error(browser, abstract, document)
        loading_status_element = locate_element_by_id(browser, abstract.county.ids["PDF Viewer Load Marker"],
                                                      "PDF Viewer load status", False, document)
    return loading_status_element.text


def wait_for_pdf_to_load(browser, abstract, document):
    while access_pdf_load_status(browser, abstract, document).startswith(abstract.county.messages["Loading"]):
        medium_nap()
        # naptime() <--- consider for testing 07/13/2023


def handle_document_image_status(browser, abstract, document):
    image_container_text = access_image_container(browser, abstract, document)
    if (image_container_text == abstract.county.messages["No Image Available"] or
       image_container_text == abstract.county.messages["Login Error"]):
        print(f'No document image exists for '
              f'{document.extrapolate_value()}, please review.')
        no_document_image(abstract, document)
        medium_nap()
        return False
    else:
        wait_for_pdf_to_load(browser, abstract, document)
        return True


def open_informational_link(browser, link):  # needs to be updated to work on a smaller screen
    center_element(browser, link)
    link.click()


def handle_information_links(browser, abstract, link):
    try:
        while link.text == abstract.county.messages["More Information"]:
            open_informational_link(browser, link)
            short_nap()
    except StaleElementReferenceException:
        print('Encountered StaleElementReferenceException '
              'while handling information links, please review.')
        input()


def review_and_open_links(browser, abstract, links):
    for link in links:
        handle_information_links(browser, abstract, link)


def display_all_information(browser, abstract, document):
    information_links = locate_elements_by_class_name(browser, abstract.county.classes["Information Links"],
                                                      "information links", False, document)
    review_and_open_links(browser, abstract, information_links)


def drop_superfluous_information(abstract, string):
    if string.endswith(abstract.county.messages["Less Information"]):
        return string[:-(len(abstract.county.messages["Less Information"]) + 1)]
    else:
        return string


def access_table_body(document_table, abstract):  # Argument order important in order to work with 'map'
    table_body = locate_element_by_tag_name(document_table, abstract.county.tags["Index Table"][0],
                                            "document table body", False, quick=True)
    while table_body is None:
        print("Unable to locate TABLE BODY element, trying again.")
        table_body = locate_element_by_tag_name(document_table, abstract.county.tags["Index Table"][0],
                                                "document table body", False, quick=True)
        naptime()
    return table_body


def access_table_rows(abstract, table_body):
    body_text = table_body.find_elements("tag name", abstract.county.tags["Index Table"][1])
    return body_text


def access_field_body_no_title(field_info):
    return "\n".join(field_info.text.split("\n")[1:])


def access_field_body(field_info):
    return "\n".join(field_info.text.split("\n")[1:]).title()


def access_indexing_information(abstract, document_table):
    table_body = access_table_body(document_table, abstract)
    table_rows = access_table_rows(abstract, table_body)
    return map(access_field_body, table_rows)


def record_document_type(abstract, document_table):
    document_type = access_title_case_text(document_table)
    record_value(abstract, 'document type', document_type)


# def split_reception_field(reception_field):
#     if "Book" in reception_field and "Page" in reception_field:
#         reception_fields = reception_field.split("\n")
#         reception_number = reception_fields[0]
#         book = reception_fields[2]
#         page = reception_fields[4]
#     else:
#         reception_number = reception_field
#         book = search_errors[2]
#         page = search_errors[2]
#     return reception_number, book, page


def set_document_download_values(abstract, document, reception_number):
    document.reception_number = reception_number
    document.download_value = f'{document.reception_number}-{abstract.county.other["Stock Download"]}'


def record_indexing_data(abstract, document_table, document):
    reception_number_recording_date_field, _ = access_indexing_information(abstract, document_table)
    reception_number, _, recording_date = reception_number_recording_date_field.split('\n')
    # reception_number, book, page = split_reception_field(reception_field)
    # reception_number = reception_number.split('\n')[0]
    set_document_download_values(abstract, document, reception_number)
    record_value(abstract, 'reception number', reception_number)
    record_value(abstract, 'recording date', recording_date[:10])


def record_book_volume_page(abstract, document_table):
    book_volume_page_field = document_table.text.split('\n')[1]
    book, volume, page = book_volume_page_field.split(' ')
    record_value(abstract, 'book', book)
    record_value(abstract, 'volume', volume)
    record_value(abstract, 'page', page)


def record_effective_date(abstract, document_table):
    effective_date_field = document_table.text
    effective_date = effective_date_field.split("\n")[1]
    record_value(abstract, 'effective date', effective_date[:10])


def record_name_data(abstract, document_table):
    grantor_text, grantee_text = access_indexing_information(abstract, document_table)
    grantor = drop_superfluous_information(abstract, grantor_text)
    grantee = drop_superfluous_information(abstract, grantee_text)
    record_value(abstract, 'grantor', grantor)
    record_value(abstract, 'grantee', grantee)


def record_legal_data(abstract, document_table):
    if document_table.text.startswith("Legal"):
        table_rows = access_table_rows(abstract, document_table)
        legal_data = table_rows[1].find_elements("tag name", abstract.county.tags["Index Table"][2])
        if legal_data == []:
            record_value(abstract, 'legal', search_errors[2])
        else:
            legal = legal_data[-1].text
            if legal.endswith(search_errors[4]):
                legal = legal.strip()  # Running along with test 1
    else:
        legal = ""
    record_value(abstract, 'legal', drop_superfluous_information(abstract, legal))


def locate_related_documents_table_rows(abstract, document, document_table):
    try:
        related_table_rows = document_table.find_elements(
            "class name",
            abstract.county.classes["Related Documents Table"])
        return related_table_rows
    except StaleElementReferenceException:
        print(f'Browser encountered StaleElementReferenceException trying to '
              f'located related documents table rows for '
              f'{document.extrapolate_value()}, trying again.')
        return False


def get_related_documents_table_rows(browser, abstract, document_table, document):
    center_element(browser, document_table)
    related_documents_table_rows = locate_related_documents_table_rows(abstract, document, document_table)
    while related_documents_table_rows is False:
        print(f'Unable to locate the "Related Documents Table" rows for '
              f'{document.extrapolate_value()}, trying again...')
        naptime()
        related_documents_table_rows = locate_related_documents_table_rows(abstract, document, document_table)
    return related_documents_table_rows


def record_related_documents(browser, abstract, document_table, document):
    # If none then ... ? conditional -- need to test with some print statements to see general feedback first
    related_table_rows = get_related_documents_table_rows(browser, abstract, document_table, document)
    related_documents_info = list(map(partial(access_table_body, abstract=abstract), related_table_rows))
    related_document_list = list(map(access_title_case_text, related_documents_info))
    # related_documents_info = list(map(access_table_body, related_table_rows))
    # related_document_list = list(map(access_title_case_text, related_documents_info))
    related_documents = "\n".join(related_document_list)
    record_value(abstract, 'related documents', drop_superfluous_information(abstract, related_documents))
    # dataframe["Related Documents"].append(drop_superfluous_information(related_documents))


def record_notes(abstract, document_tables):
    try:
        notes = access_field_body_no_title(document_tables[5])
        if notes == search_errors[3] or notes == search_errors[4] or notes == search_errors[5]:
            pass
        elif notes.startswith(search_errors[3]) or notes.endswith(search_errors[3]):
            pass
        else:
            if notes.strip() != "":
                notes = f'Notes: {notes}'
                if abstract.dataframe["Legal"][-1] == "":
                    abstract.dataframe["Legal"][-1] = notes
                else:
                    abstract.dataframe["Legal"][-1] = f'{abstract.dataframe["Legal"][-1]}\n{notes}'
    except IndexError:
        pass
    except StaleElementReferenceException:
        input('Encountered a StaleElementReferenceException, please review and press enter to continue...')


def aggregate_document_information(browser, abstract, document_tables, document):
    record_document_type(abstract, document_tables[0])
    record_indexing_data(abstract, document_tables[1], document)
    record_book_volume_page(abstract, document_tables[2])
    record_effective_date(abstract, document_tables[3])
    record_name_data(abstract, document_tables[4])
    record_legal_data(abstract, document_tables[5])
    record_related_documents(browser, abstract, document_tables[-2], document)
    record_notes(abstract, document_tables)


def access_document_tables(browser, abstract, document):
    document_information = locate_element_by_id(browser, abstract.county.ids["Document Information"],
                                                "document information", False, document)
    return locate_elements_by_class_name(document_information, abstract.county.classes["Document Table"],
                                         "document information tables", False, document)


def record_document_fields(browser, abstract, document):
    document_tables = access_document_tables(browser, abstract, document)
    display_all_information(browser, abstract, document)
    aggregate_document_information(browser, abstract, document_tables, document)
    scroll_to_top(browser)


def review_entry(browser, abstract, document):
    while (abstract.dataframe["Grantor"][-1] == abstract.county.other["Missing Values"][0] and
           abstract.dataframe["Grantee"][-1] == abstract.county.other["Missing Values"][0] and
           abstract.dataframe["Related Documents"][-1] == abstract.county.other["Missing Values"][1] or
           document.reception_number.strip() == ''):
        print("Recording of last document was processed incorrectly, attempting to record again.")
        re_record_document_fields(browser, abstract, document)


def re_record_document_fields(browser, abstract, document):
    abstract.drop_last_entry()
    browser.refresh()
    record_comments(abstract, document)
    record_empty_values(abstract, ['document link'])
    medium_nap()
    record_document_fields(browser, abstract, document)


# def access_download_information(browser, abstract, document):
#     handle_document_image_status(browser, abstract, document)
#     document_tables = access_document_tables(browser, abstract, document)
#     reception_field, _ = access_indexing_information(abstract, document_tables[1])
#     reception_number, _, _ = split_reception_field(reception_field)
#     set_document_download_values(abstract, document, reception_number)


def record(browser, abstract, document):
    print(f'Recording document located at {document.extrapolate_value()}')
    check_for_disclaimer(browser, abstract)
    medium_nap()  # Moved from the post-record in order to try and load DOM objects properly
    if not abstract.review:
        record_comments(abstract, document)  # Before 'handle_document_image_status' to check for multiple documents
        handle_document_image_status(browser, abstract, document)
        record_document_fields(browser, abstract, document)
        record_empty_values(abstract, ['document link'])
        review_entry(browser, abstract, document)
        # medium_nap()
