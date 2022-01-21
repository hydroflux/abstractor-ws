from settings.county_variables.eagle import (book_input_id, clear_search_id,
                                             download_button_id, page_input_id,
                                             reception_number_input_id,
                                             search_button_id)


def update_element_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.input_attributes = {
            "Reception Number": reception_number_input_id,
            "Book": book_input_id,
            "Page": page_input_id,
        }
        document.button_attributes = {
            "Clear Search": clear_search_id,
            "Submit Search": search_button_id,
            "Download Button": download_button_id
        }


def transform_document_list(abstract):
    update_element_attributes(abstract)
