from settings.county_variables.jaguar import (document_description_title,
                                              home_page_title, home_page_url,
                                              invalid_search_message, link_tag,
                                              login_button_name,
                                              multiple_results_message,
                                              name_input_id,
                                              no_results_text_class,
                                              number_results_class_name,
                                              reception_number_input_id,
                                              results_class_name,
                                              search_button_name,
                                              search_page_title,
                                              search_page_url,
                                              search_results_id,
                                              search_results_title,
                                              single_result_message,
                                              document_type_and_number_field_id,
                                              document_tables_tag,
                                              recording_date_field_class,
                                              validation_class_name)


# Similar to the 'leopard' & 'tiger' update_document_attributes
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


# Similar to the 'leopard' convert_document_numbers function
def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            document.value = f'{year}{document_number.zfill(6)}'


def update_county_attributes(abstract):
    abstract.county.urls = {
        # LOGIN
        "Home": home_page_url,
        # SEARCH
        "Search": search_page_url
        # DOWNLOAD
    }
    abstract.county.titles = {
        # LOGIN
        "Home": home_page_title,
        # SEARCH
        "Search": search_page_title,
        # OPEN DOCUMENT
        "Search Results": search_results_title,
        "Document Description": document_description_title,
        # DOWNLOAD
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": login_button_name,
        # SEARCH
        "Search": search_button_name
        # DOWNLOAD
    }
    abstract.county.classes = {
        # OPEN DOCUMENT
        "Number Results": number_results_class_name,
        "Results": results_class_name,
        # RECORD
        "Recording Date": recording_date_field_class,
        # VALIDATION
        "Validation": validation_class_name,
        "No Results": no_results_text_class
    }
    abstract.county.ids = {
        # OPEN DOCUMENT
        "Search Results": search_results_id,
        # RECORD
        "Document Type And Number": document_type_and_number_field_id
    }
    abstract.county.inputs = {  # Consider changing to 'SEARCH_inputs'
        # SEARCH
        "Reception Number": reception_number_input_id,
        "Name": name_input_id,
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Single Result": single_result_message,
        "Multiple Results": multiple_results_message,
        # VALIDATION
        "Invalid Search": invalid_search_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Link": link_tag,
        # RECORD
        "Document Tables": document_tables_tag
    }
    abstract.county.other = {
    }


def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
