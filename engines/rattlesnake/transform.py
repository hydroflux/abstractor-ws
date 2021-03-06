from settings.county_variables.rattlesnake import (early_book_type_id,
                                                   early_date_end_input_id,
                                                   early_date_start_input_id,
                                                   early_next_button_id,
                                                   early_page_input_id,
                                                   early_search_button_id,
                                                   early_volume_input_id,
                                                   page_image_id,
                                                   page_input_id,
                                                   page_selector_id,
                                                   reception_number_input_id,
                                                   results_table_id,
                                                   search_button_id,
                                                   volume_input_id)


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_element_attributes(abstract, early_records):
    for document in abstract.document_list:
        if early_records:
            document.input_ids = {
                "Volume": early_volume_input_id,
                "Page": early_page_input_id,
                "Date Start": early_date_start_input_id,
                "Date End": early_date_end_input_id
            }
            document.button_attributes = {
                "Submit Button": early_search_button_id,
                "Next Button": early_next_button_id
            }
            document.search_attributes = {
                "Book Type": early_book_type_id,
                "Page Image Id": page_image_id,
                "Page Selector Id": page_selector_id,
                "Results Table Id": results_table_id
            }
        else:
            document.input_attributes = {
                "Reception Number": reception_number_input_id,
                "Volume": volume_input_id,
                "Page": page_input_id,
            }
            document.button_attributes = {
                "Submit Button": search_button_id
            }


def transform_document_list(abstract, early_records=False):
    update_document_attributes(abstract)
    update_element_attributes(abstract, early_records)
