import settings.county_variables.leopard as leopard


# Similar to the 'jaguar' convert_document_numbers function
def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            if year <= 1984:
                document.value = document_number
            else:
                document.value = f'{year}{document_number.zfill(7)}'


# Identical to the 'tiger' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = leopard.stock_download


def update_county_attributes(abstract):
    abstract.county.credentials = leopard.credentials
    abstract.county.urls = {
        # LOGIN
        "Login": leopard.login_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login": leopard.login_page_title,
        # SEARCH
        "Search": leopard.search_title,
        # RECORD
        "Row Titles": leopard.row_titles
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": leopard.disclaimer_button_id,
        # SEARCH
        "Document Search": leopard.document_search_button_id,
        "Book And Page Search": leopard.book_and_page_search_button_id,
        # DOWNLOAD
        "Download Submenu": leopard.view_group_id,
        "Download": leopard.download_button_id,
        # NAVIGATION
        "Next Result": leopard.next_result_id,
        "Previous Result": leopard.previous_result_id,
        # LOGOUT
        "Logout": leopard.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Validation Error": leopard.validation_error_class,
        # DISCLAIMER
        "Disclaimer Active": leopard.disclaimer_active_class,
        # OPEN DOCUMENT
        "Result Rows": leopard.result_rows_class
    }
    abstract.county.ids = {
        # DISCLAIMER
        "Disclaimer": leopard.disclaimer_id,
        # SEARCH
        "Search Navigation": leopard.search_navigation_id,
        "Document Search Tab": leopard.document_search_tab_id,
        "Book And Page Search Tab": leopard.book_and_page_search_tab_id,
        # OPEN DOCUMENT
        "Results Count": leopard.results_count_id,
        "Results Table": leopard.results_table_id,
        # RECORD
        "Document Image": leopard.document_image_id,
        "Document Information": leopard.document_information_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": leopard.document_search_field_id,
        "Book": leopard.book_search_field_id,
        "Page": leopard.page_search_field_id
    }
    abstract.county.scripts = {
        # DISCLAIMER
        "Open Search": leopard.open_script,
        # SEARCH
        "Search": leopard.search_script
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Results Table Body": leopard.results_body_tag,
        "Result Cell": leopard.result_cell_tag,
        # RECORD
        "Document Table": leopard.document_table_tag,
        "Table Rows": leopard.table_rows_tag,
        "Row Data": leopard.row_data_tag
    }
    abstract.county.other = {
        # RECORD
        "Abbreviation": leopard.book_page_abbreviation
    }


# Identical to the 'tiger' transform_document_list function
def transform(abstract):
    convert_document_numbers(abstract)
    update_document_attributes(abstract)
    update_county_attributes(abstract)
