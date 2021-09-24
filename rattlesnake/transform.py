from rattlesnake.rattlesnake_variables import (early_date_end_input_id,
                                               early_date_start_input_id,
                                               early_page_input_id,
                                               early_search_button_id,
                                               early_volume_input_id,
                                               page_input_id,
                                               reception_number_input_id,
                                               search_button_id,
                                               volume_input_id)


def update_element_ids(document_list, early_records):
    for document in document_list:
        if early_records:
            document.input_ids = {
                "Volume": early_volume_input_id,
                "Page": early_page_input_id,
                "Date Start": early_date_start_input_id,
                "Date End": early_date_end_input_id
            }
            document.button_ids = {
                "Submit Button": early_search_button_id
            }
        else:
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


def transform_document_list(document_list, county, early_records=False):
    update_element_ids(document_list, early_records)
    update_county(document_list, county)
