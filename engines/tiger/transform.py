from settings.county_variables.tiger import stock_download, credentials


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
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.titles = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.buttons = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.classes = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.ids = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.messages = {  # Consider changing to 'search_inputs'
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.tags = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }
    abstract.county.other = {
        # LOGIN
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
    }


# Identical to the 'leopard' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
