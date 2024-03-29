import settings.county_variables.tiger as tiger


# Identical to the 'leopard' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = tiger.stock_download


def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            if document.year <= 2004:
                input("Please review previously written code in order to create a more robust transformation script.")
            else:
                document.value = f'{year}{document_number.zfill(9)}'


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
        # DISCLAIMER
        "Disclaimer": tiger.disclaimer_button_id,
        # LOGIN
        "Login": tiger.login_button_name,
        # "Disclaimer": tiger.handle_disclaimer_button_id,
        # SEARCH
        # "Search": tiger.search_button_id,
        # SEARCH
        "Document Search": tiger.document_search_button_id,
        "Book And Page Search": tiger.book_and_page_search_button_id,
        # OPEN DOCUMENT
        "Result Count": tiger.result_count_button_id,
        # DOWNLOAD
        "Download Submenu": tiger.download_submenu_id,
        "Download": tiger.download_button_id,
        # NAVIGATION
        "Next Result": tiger.next_result_id,
        "Previous Result": tiger.previous_result_id,
    }
    abstract.county.classes = {
        # DISCLAIMER
        "Disclaimer Active": tiger.disclaimer_active_class,
        # OPEN DOCUMENT
        "Result Rows": tiger.result_rows_class
    }
    abstract.county.ids = {
        # DISCLAIMER
        "Disclaimer": tiger.disclaimer_id,
        # SEARCH
        # "Search Navigation": tiger.search_navigation_id,
        # "Search Tab": tiger.search_tab_id,
        # SEARCH
        "Search Navigation": tiger.search_navigation_id,
        "Document Search Tab": tiger.document_search_tab_id,
        "Book And Page Search Tab": tiger.book_and_page_search_tab_id,
        # OPEN DOCUMENT
        "Result Count": tiger.result_count_id,
        # "Results Table": tiger.results_table_id,
        # OPEN DOCUMENT
        "Results Count": tiger.results_count_id,
        "Results Table": tiger.results_table_id,
        # RECORD
        "Document Image": tiger.document_image_id,
        "Document Information": tiger.document_information_id,
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": tiger.document_search_field_id,
        "Book": tiger.book_search_field_id,
        "Page": tiger.page_search_field_id
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Counting": tiger.counting_results
    }
    abstract.county.scripts = {
        # DISCLAIMER
        "Open Search": tiger.open_script,
        # SEARCH
        "Search": tiger.search_script
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Results Table Body": tiger.results_body_tag,
        "Result Cell": tiger.result_cell_tag,
        # OPEN / RECORD DOCUMENT
        "Body": tiger.results_body_tag,
        "Rows": tiger.first_result_tag,
        "Data": tiger.result_cell_tag,
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
