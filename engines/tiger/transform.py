from settings.county_variables.tiger import (credentials,
                                             document_search_field_id,
                                             first_result_tag,
                                             handle_disclaimer_button_id,
                                             login_button_name, login_page,
                                             login_title, result_cell_tag,
                                             result_count_button_id,
                                             result_count_id, results_body_tag,
                                             results_table_id,
                                             search_button_id,
                                             search_navigation_id,
                                             search_script, search_tab_id,
                                             search_title, stock_download)


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
        # RECORD
        # DOWNLOAD
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_title,
        # SEARCH
        "Search": search_title,
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
        "Result Count": result_count_button_id,
        # RECORD
        # DOWNLOAD
    }
    abstract.county.classes = {
        # RECORD
        # DOWNLOAD
    }
    abstract.county.ids = {
        # SEARCH
        "Search Navigation": search_navigation_id,
        "Search Tab": search_tab_id,
        # OPEN DOCUMENT
        "Result County": result_count_id,
        "Results Table": results_table_id,
        # RECORD
        # DOWNLOAD
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": document_search_field_id
        # RECORD
        # DOWNLOAD
    }
    abstract.county.messages = {  # Consider changing to 'search_inputs'
        # RECORD
        # DOWNLOAD
    }
    abstract.county.scripts = {
        # SEARCH
        "Search": search_script,
        # RECORD
        # DOWNLOAD
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Body": results_body_tag,
        "Row": first_result_tag,
        "Cell": result_cell_tag,
        # RECORD
        # DOWNLOAD
    }
    abstract.county.other = {
        # RECORD
        # DOWNLOAD
    }


# Identical to the 'leopard' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
