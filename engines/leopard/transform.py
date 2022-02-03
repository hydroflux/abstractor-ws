from settings.county_variables.leopard import stock_download


# Identical to the 'tiger' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = stock_download


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


def update_county_attributes(abstract):
    abstract.county.urls = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.titles = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.buttons = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.classes = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.ids = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.messages = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.tags = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }
    abstract.county.other = {
        # LOGIN
        # DISCLAIMER
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # NAVIGATION
        # LOGOUT
    }


# Identical to the 'tiger' transform_document_list function
def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
