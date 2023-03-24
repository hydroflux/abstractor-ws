from engines.buffalo.frame_handling import (
    switch_to_document_information_frame,
    switch_to_related_documents_menu_frame)
from engines.buffalo.validation import check_for_document_image, page_is_loaded

from selenium_utilities.element_interaction import access_title_case_text
from selenium_utilities.locators import locate_element

from serializers.recorder import (record_comments, record_empty_values,
                                  record_value)
from settings.general_functions import four_character_padding


def record_document_type(browser, abstract, document):
    document_type_element = locate_element(browser, "xpath", abstract.county.xpaths["Document Type"],
                                           "document type", False, document)
    document_type = access_title_case_text(document_type_element)
    record_value(abstract, "document type", document_type)


def set_document_download_values(document, reception_number):
    document.reception_number = reception_number
    if document.type == "document_number":
        document.download_value = f'{reception_number}.pdf'
    elif document.type == "book_and_page":
        book, page = document.document_value()
        document.download_value = f'{four_character_padding(book)}-{four_character_padding(page)}.pdf'
        document.alternate_download_value = f'{reception_number}.pdf'
        document.target_name = f'{document.county.prefix}-{reception_number}.pdf'
        document.target_type = "document_number"


def record_reception_number(browser, abstract, document):
    reception_number_element = locate_element(browser, "xpath", abstract.county.xpaths["Reception Number"],
                                              "reception number", False, document)
    reception_number = reception_number_element.text
    set_document_download_values(document, reception_number)
    record_value(abstract, "reception number", reception_number)


def record_book(browser, abstract, document):
    book_element = locate_element(browser, "xpath", abstract.county.xpaths["Book"],
                                  "book", False, document)
    book = book_element.text.strip()
    if book == "":
        record_value(abstract, "book", "N/A")
    else:
        record_value(abstract, "book", book)


def record_page(browser, abstract, document):
    page_element = locate_element(browser, "xpath", abstract.county.xpaths["Page"],
                                  "page", False, document)
    page = page_element.text.strip()
    if page == "":
        record_value(abstract, "page", "N/A")
    else:
        record_value(abstract, "page", page)


def record_recording_date(browser, abstract, document):
    recording_date = locate_element(browser, "xpath", abstract.county.xpaths["Recording Date"],
                                    "recording date", False, document)
    recording_date = recording_date.text[:10]
    record_value(abstract, "recording date", recording_date)


def string_list_string(string, deliminator):
    split_string = string.split(deliminator)
    string_list = []
    for i in split_string:
        string_list.append(i.strip())
    return "\n".join(string_list)


def record_grantor(browser, abstract, document):
    grantor_element = locate_element(browser, "xpath", abstract.county.xpaths["Grantor"],
                                     "grantor", False, document)
    if grantor_element is not None:
        grantor_list_string = access_title_case_text(grantor_element)
        grantor = string_list_string(grantor_list_string, "\n")
    else:
        grantor = ""
    record_value(abstract, "grantor", grantor)


def record_grantee(browser, abstract, document):
    grantee_element = locate_element(browser, "xpath", abstract.county.xpaths["Grantee"],
                                              "grantee", False, document)
    if grantee_element is not None:
        grantee_list_string = access_title_case_text(grantee_element)
        grantee = string_list_string(grantee_list_string, "\n")
    else:
        grantee = ""
    record_value(abstract, "grantee", grantee)


def drop_invalid_legal_description(abstract, legal):
    invalid_legal = abstract.county.messages["Invalid Legal"]
    if legal.startswith(invalid_legal):
        if legal == invalid_legal:
            legal = ""
        else:
            legal = legal[len(invalid_legal):]
    return legal


def record_legal(browser, abstract, document):
    legal_elements = []
    for path in abstract.county.xpaths["Legal"]:
        element = locate_element(browser, "xpath", path, "legal", False, document, True)
        if element is not None and element.text.strip() != "":
            legal_elements.append(element.text.strip())
    print("legal_elements_list", legal_elements)
    legal = "\n".join(legal_elements).strip()
    updated_legal = drop_invalid_legal_description(abstract, legal)
    record_value(abstract, "legal", updated_legal)


def access_related_documents(browser, abstract, document):
    try:
        switch_to_related_documents_menu_frame(browser, abstract)
        related_documents_button = locate_element(browser, "classes", abstract.county.buttons["Related Documents"],
                                                  "related documents button", True, document)[1]
        related_documents_button.click()
        return True
    except IndexError:
        return False


def record_related_documents(browser, abstract, document):
    if access_related_documents(browser, abstract, document):
        switch_to_document_information_frame(browser, abstract)
        related_documents_elements = []
        for path in abstract.county.xpaths["Related Documents"]:
            element = locate_element(browser, "xpath", path, "related documents", False, document, True)
            element_text = element.text.strip()
            if element_text != abstract.county.messages["No Related Documents"]:
                related_documents_elements.append(element_text)
        related_documents_list_string = "\n".join(related_documents_elements)
        related_documents = string_list_string(related_documents_list_string, "\n")
    else:
        related_documents = ""
    record_value(abstract, "related documents", related_documents)


def record_document_information(browser, abstract, document):
    switch_to_document_information_frame(browser, abstract)
    record_document_type(browser, abstract, document)
    record_reception_number(browser, abstract, document)
    record_book(browser, abstract, document)
    record_page(browser, abstract, document)
    record_recording_date(browser, abstract, document)
    record_grantor(browser, abstract, document)
    record_grantee(browser, abstract, document)
    record_legal(browser, abstract, document)
    record_related_documents(browser, abstract, document)
    record_comments(abstract, document)


def record(browser, abstract, document):
    # naptime()?
    if page_is_loaded(browser, abstract, abstract.county.messages["Document Information"]):
        if not abstract.review:
            record_document_information(browser, abstract, document)
            record_empty_values(abstract, ['effective date', 'volume', 'document link'])
            check_for_document_image(browser, abstract, document)
