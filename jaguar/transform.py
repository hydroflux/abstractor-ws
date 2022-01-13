from settings.county_variables.jaguar import (reception_number_input_id, name_input_id, search_button_name)


def update_county(document_list, county):
    for document in document_list:
        document.county = county


def update_element_attributes(document_list):
    for document in document_list:
        document.input_attributes = {
            "Reception Number": reception_number_input_id,
            "Name": name_input_id
        }
        document.button_attributes = {
            "Submit Search": search_button_name
        }


def transform_document_list(document_list, county):
    update_county(document_list, county)
    update_element_attributes(document_list)
