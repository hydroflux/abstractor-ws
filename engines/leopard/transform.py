from settings.county_variables.leopard import (credentials, login_page_title,
                                               login_page_url,
                                               logout_button_id,
                                               stock_download,
                                               validation_error_class,
                                               validation_error_message)


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
        "Login": login_page_url
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_page_title
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.buttons = {
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
        "Logout": logout_button_id
    }
    abstract.county.classes = {
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
        "Validation Error": validation_error_class
    }
    abstract.county.ids = {
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.messages = {
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
        "Validation Error": validation_error_message
    }
    abstract.county.tags = {
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.other = {
        # DISCLAIMER
        # SEARCH
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
