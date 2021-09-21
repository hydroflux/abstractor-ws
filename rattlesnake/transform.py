from rattlesnake.rattlesnake_variables import (
    page_input_id, reception_number_input_id, search_button_id,
    volume_input_id)


def convert_document_numbers(document_list):
    pass


def update_element_ids(document_list):
    for document in document_list:
        document.input_ids = {
            "Reception Number": reception_number_input_id,
            "Volume": volume_input_id,
            "Page": page_input_id,
            }
        document.button_ids = {
            "Submit Button": search_button_id
        }


def update_county(document_list, county):
    for document in document_list:
        document.county = county


def transform_document_list(document_list, county):
    convert_document_numbers(document_list)
    update_element_ids(document_list)
    update_county(document_list, county)
