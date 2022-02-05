import settings.county_variables.tiger as tiger


# Identical to the 'leopard' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = tiger.stock_download


def convert_document_numbers(abstract):
    # Use the leopard 'transform' script as a model
    pass


def update_county_attributes(abstract):
    abstract.county.credentials = tiger.credentials
    abstract.county.urls = {
        # LOGIN
        "Login": tiger.login_page
    }
    abstract.county.titles = {
        # LOGIN
        "Login": tiger.login_title,
        # SEARCH
        "Search": tiger.search_title,
        # RECORD
        "Row Titles": tiger.row_titles
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": tiger.login_button_name,
        "Disclaimer": tiger.handle_disclaimer_button_id,
        # SEARCH
        "Search": tiger.search_button_id,
        # OPEN DOCUMENT
        "Result Count": tiger.result_count_button_id,
        # DOWNLOAD
        "Download Submenu": tiger.view_panel_id,
        "Download": tiger.download_button_id
    }
    abstract.county.classes = {
    }
    abstract.county.ids = {
        # SEARCH
        "Search Navigation": tiger.search_navigation_id,
        "Search Tab": tiger.search_tab_id,
        # OPEN DOCUMENT
        "Result County": tiger.result_count_id,
        "Results Table": tiger.results_table_id,
        # RECORD
        "Document Image": tiger.document_image_id,
        "Document Information": tiger.document_information_id,
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": tiger.document_search_field_id
    }
    abstract.county.messages = {  # Consider changing to 'search_inputs'
    }
    abstract.county.scripts = {
        # SEARCH
        "Search": tiger.search_script
    }
    abstract.county.tags = {
        # OPEN / RECORD DOCUMENT
        "Body": tiger.results_body_tag,
        "Rows": tiger.first_result_tag,
        "Data": tiger.result_cell_tag,
        # "Body": document_table_tag,
        # "Rows": table_row_tag,
        # "Data": row_data_tag
    }
    abstract.county.other = {
        # RECORD
        "Abbreviation": tiger.book_page_abbreviation
    }


# Identical to the 'leopard' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
