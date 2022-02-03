from settings.county_variables.jaguar import (home_page_title, home_page_url,
                                              login_button_name, name_input_id,
                                              reception_number_input_id,
                                              search_button_name,
                                              search_page_title,
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
        "Search": search_page_title
        # OPEN DOCUMENT
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
        "Name": name_input_id
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # VALIDATION
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
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
