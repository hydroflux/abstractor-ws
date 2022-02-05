from settings.county_variables.tiger import (credentials, search_script, search_navigation_id,
                                             handle_disclaimer_button_id, search_title, search_tab_id, search_button_id, document_search_field_id,
                                             login_button_name, login_page,
                                             login_title, stock_download)


# Identical to the 'leopard' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = stock_download


def convert_document_numbers(abstract):
    # Use the leopard 'transform' script as a model
    pass


def update_county_attributes(abstract):
    abstract.county.credentials = credentials
    abstract.county.urls = {
        # LOGIN
        "Login": login_page,
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_title,
        # SEARCH
        "Search": search_title,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": login_button_name,
        "Disclaimer": handle_disclaimer_button_id,
        # SEARCH
        "Search": search_button_id,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.classes = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.ids = {
        # SEARCH
        "Search Navigation": search_navigation_id,
        "Search Tab": search_tab_id,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": document_search_field_id
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.messages = {  # Consider changing to 'search_inputs'
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.scripts = {
        # SEARCH
        "Search": search_script,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.tags = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.other = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }


# Identical to the 'leopard' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
