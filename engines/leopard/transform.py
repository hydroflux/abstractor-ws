from settings.county_variables.leopard import (credentials, login_page_title, open_script, disclaimer_id,
                                               login_page_url, disclaimer_active_class, disclaimer_button_id,
                                               logout_button_id,
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
        "Login": login_page_url
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.titles = {
        # LOGIN
        "Login": login_page_title
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": disclaimer_button_id,
        # SEARCH
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
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
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
        # DISCLAIMER
        "Open Script": open_script,
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
