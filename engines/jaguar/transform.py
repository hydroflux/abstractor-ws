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
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.titles = {
        # LOGIN
        "Home": home_page_title,
        # SEARCH
        "Search": search_page_title,
        # OPEN DOCUMENT
        "Results": search_results_title,
        "Document Description": document_description_title,
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": login_button_name,
        # SEARCH
        "Search": search_button_name
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.classes = {
        # OPEN DOCUMENT
        "Number Results": number_results_class_name,
        "Results": results_class_name,
        # RECORD
        # DOWNLOAD
        # VALIDATION
        "Validation": validation_class_name,
        "No Results": no_results_text_class
    }
    abstract.county.ids = {
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.inputs = {  # Consider changing to 'SEARCH_inputs'
        # SEARCH
        "Reception Number": reception_number_input_id,
        "Name": name_input_id,
        # OPEN DOCUMENT
        "Search Results": search_results_id,
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Single Result": single_result_message,
        "Multiple Results": multiple_results_message,
        # RECORD
        # DOWNLOAD
        # VALIDATION
        "Invalid Search": invalid_search_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Link": link_tag
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.other = {
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }


def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
