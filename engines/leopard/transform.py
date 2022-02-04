from settings.county_variables.leopard import (book_and_page_search_button_id,
                                               book_and_page_search_tab_id,
                                               book_search_field_id, credentials,
                                               disclaimer_active_class,
                                               disclaimer_button_id,
                                               disclaimer_id,
                                               document_search_button_id,
                                               document_search_field_id,
                                               document_search_tab_id,
                                               login_page_title,
                                               login_page_url,
                                               logout_button_id, open_script,
                                               page_search_field_id,
                                               search_navigation_id,
                                               search_script, search_title,
                                               stock_download,
                                               validation_error_class)


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
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_page_title,
        # SEARCH
        "Search": search_title
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": disclaimer_button_id,
        # SEARCH
        "Document Search": document_search_button_id,
        "Book And Page Search": book_and_page_search_button_id,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
        "Logout": logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Validation Error": validation_error_class,
        # DISCLAIMER
        "Disclaimer Active": disclaimer_active_class,
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.ids = {
        # DISCLAIMER
        "Disclaimer": disclaimer_id,
        # SEARCH
        "Search Navigation": search_navigation_id,
        "Document Search Tab": document_search_tab_id,
        "Book And Page Search Tab": book_and_page_search_tab_id
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": document_search_field_id,
        "Book": book_search_field_id,
        "Page": page_search_field_id,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.messages = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.tags = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.other = {
        # SEARCH
        "Open Script": open_script,  # DISCLAIMER & SEARCH
        "Search Script": search_script,  # DISCLAIMER & SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }


# Identical to the 'tiger' transform_document_list function
def transform(abstract):
    convert_document_numbers(abstract)
    update_document_attributes(abstract)
    update_county_attributes(abstract)
