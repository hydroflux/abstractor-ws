import settings.county_variables.jaguar as jaguar


# Similar to the 'leopard' & 'tiger' update_document_attributes
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


# Similar to the 'leopard' convert_document_numbers function
def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            document.value = f'{year}{document_number.zfill(6)}'


def update_county_attributes(abstract):
    abstract.county.urls = {
        # LOGIN
        "Home": jaguar.home_page_url,
        # SEARCH
        "Search": jaguar.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home": jaguar.home_page_title,
        # SEARCH
        "Search": jaguar.search_page_title,
        # OPEN DOCUMENT
        "Search Results": jaguar.search_results_title,
        "Document Description": jaguar.document_description_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": jaguar.login_button_name,
        # SEARCH
        "Search": jaguar.search_button_name,
        # DOWNLOAD
        "Download": jaguar.download_button_class
    }
    abstract.county.classes = {
        # OPEN DOCUMENT
        "Number Results": jaguar.number_results_class_name,
        "Results": jaguar.results_class_name,
        # RECORD
        "Recording Date": jaguar.recording_date_field_class,
        # VALIDATION
        "Validation": jaguar.validation_class_name,
        "No Results": jaguar.no_results_text_class
    }
    abstract.county.ids = {
        # OPEN DOCUMENT
        "Search Results": jaguar.search_results_id,
        # RECORD
        "Document Type And Number": jaguar.document_type_and_number_field_id
    }
    abstract.county.inputs = {  # Consider changing to 'SEARCH_inputs'
        # SEARCH
        "Reception Number": jaguar.reception_number_input_id,
        "Name": jaguar.name_input_id
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Single Result": jaguar.single_result_message,
        "Multiple Results": jaguar.multiple_results_message,
        # VALIDATION
        "Invalid Search": jaguar.invalid_search_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Link": jaguar.link_tag,
        # RECORD
        "Document Tables": jaguar.document_tables_tag
    }


def transform(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
    update_county_attributes(abstract)
