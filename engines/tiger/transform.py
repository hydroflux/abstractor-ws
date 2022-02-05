from settings.county_variables.tiger import (book_page_abbreviation,
                                             credentials, document_image_id,
                                             document_information_id,
                                             document_search_field_id,
                                             download_button_id,
                                             first_result_tag,
                                             handle_disclaimer_button_id,
                                             login_button_name, login_page,
                                             login_title, result_cell_tag,
                                             result_count_button_id,
                                             result_count_id, results_body_tag,
                                             results_table_id, row_titles,
                                             search_button_id,
                                             search_navigation_id,
                                             search_script, search_tab_id,
                                             search_title, stock_download,
                                             view_panel_id)


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
        "Login": login_page
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_title,
        # SEARCH
        "Search": search_title,
        # RECORD
        "Row Titles": row_titles
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": login_button_name,
        "Disclaimer": handle_disclaimer_button_id,
        # SEARCH
        "Search": search_button_id,
        # OPEN DOCUMENT
        "Result Count": result_count_button_id,
        # DOWNLOAD
        "Download": download_button_id
    }
    abstract.county.classes = {
    }
    abstract.county.ids = {
        # SEARCH
        "Search Navigation": search_navigation_id,
        "Search Tab": search_tab_id,
        # OPEN DOCUMENT
        "Result County": result_count_id,
        "Results Table": results_table_id,
        # RECORD
        "Document Image": document_image_id,
        "Document Information": document_information_id,
        # DOWNLOAD
        "View Panel": view_panel_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": document_search_field_id
    }
    abstract.county.messages = {  # Consider changing to 'search_inputs'
    }
    abstract.county.scripts = {
        # SEARCH
        "Search": search_script
    }
    abstract.county.tags = {
        # OPEN / RECORD DOCUMENT
        "Body": results_body_tag,
        "Rows": first_result_tag,
        "Data": result_cell_tag,
        # "Body": document_table_tag,
        # "Rows": table_row_tag,
        # "Data": row_data_tag
    }
    abstract.county.other = {
        # RECORD
        "Abbreviation": book_page_abbreviation
    }


# Identical to the 'leopard' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
