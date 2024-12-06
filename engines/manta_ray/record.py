from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)
from serializers.recorder import (date_from_string, list_to_string,
                                  record_comments, record_empty_values,
                                  record_value, remove_empty_list_items,
                                  title_strip)
from settings.general_functions import get_direct_children

# Similar code functionality in "dolphin",  "manta_ray", & "swordfish"


def record_document_type(browser, abstract, document):
    document_type_field = locate_element_by_class_name(browser, abstract.county.record["Document Type"],
                                                       "document type", False, document)
    record_value(abstract, 'document type', document_type_field.text.title())


def set_indexing_text(text_element):
    indexing_text = text_element.text.split('\n')
    while not indexing_text[-1].startswith("R"):
        indexing_text = indexing_text[:-1]
    return indexing_text


def record_book(abstract, book_text):
    book = book_text.split(' ')[1]
    record_value(abstract, 'book', book)


def record_page(abstract, page_text):
    page = page_text.split(' ')[1]
    record_value(abstract, 'page', page)


def record_effective_date(abstract, effective_date_text):
    if effective_date_text != "":
        effective_date = date_from_string(effective_date_text.split(' ')[-1])
    record_value(abstract, 'effective date', effective_date)


def record_recording_date(abstract, recording_date_text):
    recording_date = date_from_string(recording_date_text.split(' ')[2])
    record_value(abstract, 'recording date', recording_date)
    return recording_date


def set_document_download_values(document, reception_number, document_link):
    document.reception_number = reception_number
    document.download_value = f'{reception_number}.pdf'
    document.target_name = f'{document.county.prefix}-{document_link}.pdf'


def record_reception_number(abstract, document, reception_number_text, recording_date):
    reception_number = reception_number_text[1:]
    document_link = f'{recording_date[-4:]}-{reception_number}'
    set_document_download_values(document, reception_number, document_link)
    record_value(abstract, 'reception number', reception_number)
    record_value(abstract, 'document link', document_link)


def record_indexing_information(browser, abstract, document):
    indexing_information_container = locate_element_by_id(browser, abstract.county.record["Indexing Information"],
                                                          "indexing information", False, document)
    indexing_text = set_indexing_text(indexing_information_container)
    if len(indexing_text) == 5:
        reception_number_text, book_text, page_text, effective_date_text, recording_date_text = indexing_text
        # else:
        #     if indexing_text[1].startswith("B"):
        #         reception_number_text, book_and_page_text, recording_date_text = indexing_text
        #         effective_date_text = ""
        #     else:
        #         reception_number_text, effective_date_text, recording_date_text = indexing_text
        #         book_and_page_text = None
        record_book(abstract, book_text)
        record_page(abstract, page_text)
        record_effective_date(abstract, effective_date_text)
        recording_date = record_recording_date(abstract, recording_date_text)
        record_reception_number(abstract, document, reception_number_text, recording_date)
    else:
        input('Unexpected result while parsing indexing information, please review and update accordingly...')


def record_parties(browser, abstract, document):
    parties_container = locate_element_by_id(browser, abstract.county.record["Parties"], "parties", False, document)
    parties_text_list = remove_empty_list_items(parties_container.text.split('\n'))
    midpoint = parties_text_list.index('Grantees')
    grantor = list(map(title_strip, parties_text_list[1:midpoint]))
    grantee = list(map(title_strip, parties_text_list[(midpoint + 1):]))
    record_value(abstract, 'grantor', list_to_string(grantor))
    record_value(abstract, 'grantee', list_to_string(grantee))


def access_notes(browser, abstract, document):
    notes_container = locate_element_by_id(browser, abstract.county.record["Notes"], "notes", False, document)
    notes_text = get_direct_children(notes_container)[2].text
    if notes_text.startswith('Legals'):
        return list_to_string(notes_text.split('\n')[1:])
    elif notes_text.startswith('Notes'):
        return list_to_string(notes_text.split(' ')[1:], False)
    else:
        input('Unexpected result while parsing notes, please review and update accordingly...')


def record_legal(browser, abstract, document):
    legal_field = locate_element_by_class_name(browser, abstract.county.record["Legal"], "legal", False, document)
    legal = list_to_string(legal_field.text.split('\n')[1:])
    notes = access_notes(browser, abstract, document)
    if notes == legal or notes.strip() == '':
        record_value(abstract, 'legal', legal)
    else:
        record_value(abstract, 'legal', f'{notes.strip()}\n\n{legal}')


def record_related_documents(browser, abstract, document):
    related_documents_field = locate_element_by_class_name(browser, abstract.county.record["Related Documents"],
                                                           "related documents", False, document)
    related_documents = list_to_string(related_documents_field.text.split('\n')[1:])
    record_value(abstract, 'related documents', related_documents)


def record_document_fields(browser, abstract, document):
    record_document_type(browser, abstract, document)
    record_indexing_information(browser, abstract, document)
    record_parties(browser, abstract, document)
    record_legal(browser, abstract, document)
    record_related_documents(browser, abstract, document)
    record_empty_values(abstract, ['volume'])
    record_comments(abstract, document)


def record(browser, abstract, document):
    if not abstract.review:
        record_document_fields(browser, abstract, document)
