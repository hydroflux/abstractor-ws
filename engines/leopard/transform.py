from settings.county_variables.leopard import (book_and_page_search_button_id,
                                               book_and_page_search_tab_id,
                                               book_page_abbreviation,
                                               book_search_field_id,
                                               credentials,
                                               disclaimer_active_class,
                                               disclaimer_button_id,
                                               disclaimer_id,
                                               document_image_id,
                                               document_information_id,
                                               document_search_button_id,
                                               document_search_field_id,
                                               document_search_tab_id,
                                               document_table_tag,
                                               download_button_id,
                                               login_page_title,
                                               login_page_url,
                                               logout_button_id,
                                               next_result_id, open_script,
                                               page_search_field_id,
                                               previous_result_id,
                                               result_cell_tag,
                                               result_rows_class,
                                               results_body_tag,
                                               results_count_id,
                                               results_table_id, row_data_tag,
                                               row_titles,
                                               search_navigation_id,
                                               search_script, search_title,
                                               stock_download, table_rows_tag,
                                               validation_error_class,
                                               view_group_id)


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
        document.download_value = stock_download


def update_county_attributes(abstract):
    abstract.county.credentials = credentials
    abstract.county.urls = {
        # LOGIN
        "Login": login_page_url,
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_page_title,
        # SEARCH
        "Search": search_title,
        # RECORD
        "Row Titles": row_titles
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": disclaimer_button_id,
        # SEARCH
        "Document Search": document_search_button_id,
        "Book And Page Search": book_and_page_search_button_id,
        # DOWNLOAD
        "Download Submenu": view_group_id,
        "Download": download_button_id,
        # NAVIGATION
        "Next Result": next_result_id,
        "Previous Result": previous_result_id,
        # LOGOUT
        "Logout": logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Validation Error": validation_error_class,
        # DISCLAIMER
        "Disclaimer Active": disclaimer_active_class,
        # OPEN DOCUMENT
        "Result Rows": result_rows_class,
    }
    abstract.county.ids = {
        # DISCLAIMER
        "Disclaimer": disclaimer_id,
        # SEARCH
        "Search Navigation": search_navigation_id,
        "Document Search Tab": document_search_tab_id,
        "Book And Page Search Tab": book_and_page_search_tab_id,
        # OPEN DOCUMENT
        "Results Count": results_count_id,
        "Results Table": results_table_id,
        # RECORD
        "Document Image": document_image_id,
        "Document Information": document_information_id,
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": document_search_field_id,
        "Book": book_search_field_id,
        "Page": page_search_field_id,
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Results Table Body": results_body_tag,
        "Result Cell": result_cell_tag,
        # RECORD
        "Document Table": document_table_tag,
        "Table Rows": table_rows_tag,
        "Row Data": row_data_tag,
    }
    abstract.county.other = {
        # SEARCH
        "Open Script": open_script,  # DISCLAIMER & SEARCH
        "Search Script": search_script,
        # RECORD
        "Abbreviation": book_page_abbreviation
    }


# Identical to the 'tiger' transform_document_list function
def transform(abstract):
    convert_document_numbers(abstract)
    update_document_attributes(abstract)
    update_county_attributes(abstract)
