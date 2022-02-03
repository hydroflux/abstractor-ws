from settings.county_variables.jaguar import (home_page_title, home_page_url,
                                              login_button_name, name_input_id,
                                              reception_number_input_id,
                                              search_button_name,
                                              search_page_title, search_results_title, number_results_class_name,
                                              single_result_message, multiple_results_message, search_results_id,
                                              results_class_name, link_tag, document_description_title,
                                              search_page_url)


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
    # abstract.county.credentials = credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Home": home_page_url,
        # SEARCH
        "Search": search_page_url
        # OPEN DOCUMENT
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
        # OPEN DOCUMENT
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
    }
    abstract.county.ids = {
        # OPEN DOCUMENT
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
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Link": link_tag
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.other = {
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }


def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
