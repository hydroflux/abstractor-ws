from rattlesnake.rattlesnake_variables import (old_date_end_input_id,
                                               old_date_start_input_id,
                                               old_page_input_id,
                                               old_volume_input_id,
                                               page_input_id,
                                               reception_number_input_id,
                                               search_button_id,
                                               volume_input_id)


def update_element_ids(document_list):
    for document in document_list:
        if document.year >= '1985' or document.year is None:
            document.input_ids = {
                "Reception Number": reception_number_input_id,
                "Volume": volume_input_id,
                "Page": page_input_id,
                }
            document.button_ids = {
                "Submit Button": search_button_id
            }
        else:
            document.input_ids = {
                "Volume": old_volume_input_id,
                "Page": old_page_input_id,
                "Date Start": old_date_start_input_id,
                "Date End": old_date_end_input_id
            }


def update_county(document_list, county):
    for document in document_list:
        document.county = county


def transform_document_list(document_list, county):
    update_element_ids(document_list)
    update_county(document_list, county)
