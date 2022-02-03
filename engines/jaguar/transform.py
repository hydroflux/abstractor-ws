from settings.county_variables.jaguar import (name_input_id,
                                              reception_number_input_id,
                                              search_button_name)


# Similar to the 'leopard' & 'tiger' update_document_attributes
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


# Similar to the 'leopard' convert_document_numbers function
def convert_document_numbers(abstract):
    # abstract.county.credentials = credentials  # Login
    abstract.county.urls = {
        # Login
        # Search
    }
    abstract.county.titles = {
        # Login
    }
    abstract.county.buttons = {
        # Login
        # Disclaimer
        # Search
        # Download
    }
    abstract.county.classes = {
        # Login
        # Open Document
        # Record
        # Download
        # Error Handling
    }
    abstract.county.ids = {
        # Record
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # Search
    }
    abstract.county.messages = {
        # Login
        # Open Document
        # Record
        # Error Handling
    }
    abstract.county.tags = {
        # Open Document
        # Record
    }
    abstract.county.other = {
        # Disclaimer
        # Record
    }


def update_county_attributes(abstract):

    for document in abstract.document_list:
        document.input_attributes = {
            "Reception Number": reception_number_input_id,
            "Name": name_input_id
        }
        document.button_attributes = {
            "Submit Search": search_button_name
        }


def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
