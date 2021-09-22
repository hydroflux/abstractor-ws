from eagle.eagle_variables import (book_input_id, clear_search_id,
                                   login_button_id, page_input_id,
                                   reception_number_input_id, search_button_id)


def update_element_ids(document_list):
    for document in document_list:
        document.input_ids = {
            "Reception Number": reception_number_input_id,
            "Book": book_input_id,
            "Page": page_input_id,
        }
        document.button_ids = {
            "Login": login_button_id,
            "Clear Search": clear_search_id,
            "Submit Search": search_button_id
        }


def update_county(document_list, county):
    for document in document_list:
        document.county = county


def transform_document_list(document_list, county):
    update_element_ids(document_list)
    update_county(document_list, county)
