import settings.county_variables.jaguar as jaguar


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = jaguar.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Home Page": jaguar.home_page_url,
        # "Fallback Search": jaguar.fallback_search_url,
        # "Log Out Redirect": jaguar.logged_out_redirect_url,
        # SEARCH
        # "Search Page": jaguar.search_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home Page": jaguar.home_page_title,
        # SEARCH
        # "Search Page": jaguar.search_title,
        # OPEN DOCUMENT
        # "Document Description": jaguar.document_description_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Disclaimer": jaguar.disclaimer_button_id,
        # "Login": jaguar.login_button_id,
        # SEARCH
        # "Clear Search": jaguar.clear_search_id,
        # "Submit Search": jaguar.search_button_id,
        # DOWNLOAD
        # "Download Button": jaguar.download_button_id
    }
    abstract.county.classes = {
        # OPEN DOCUMENT
        # "Validation": jaguar.validation_class_name,
        # "Results Row": jaguar.results_row_class_name,
        # "Result Actions": jaguar.result_actions_class_name,
        # RECORD
        # "Document Table": jaguar.document_table_class,
        # "Information Links": jaguar.information_links_class,
        # "Related Documents Table": jaguar.related_table_class,
        # DOWNLOAD
        # "PDF Viewer": jaguar.pdf_viewer_class_name,
        # "Purchase Button": jaguar.purchase_button_class_name,
        # NAVIGATION
        # "Result Buttons": jaguar.result_buttons_class,
        # ERROR HANDLING
        # "Error Message": jaguar.error_message_class
    }
    abstract.county.ids = {
        # LOGIN
        "Login Prompt": jaguar.login_prompt_id,
        # RECORD
        # "Image Container": jaguar.image_container_id,
        # "Document Information": jaguar.document_information_id,
        # "PDF Viewer Load Marker": jaguar.pdf_viewer_load_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        # "Reception Number": jaguar.reception_number_input_id,
        # "Book": jaguar.book_input_id,
        # "Page": jaguar.page_input_id,
        # "Name": jaguar.name_input_id,
        # "Start Date": jaguar.start_date_id,
        # "End Date": jaguar.end_date_id
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        # "Currently Searching": jaguar.currently_searching,
        # "No Results": jaguar.no_results_message,
        # "Failed Search": jaguar.failed_search,
        # "Invalid Search": jaguar.invalid_search_message,
        # RECORD
        # "No Image Available": jaguar.no_image_message,
        # "Loading": jaguar.loading_status,
        # "More Information": jaguar.more_info_message,
        # "Less Information": jaguar.less_info_message,
        # "Login Error": jaguar.login_error_message,
        # ERROR HANDLING
        # "Error Message": jaguar.error_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        # "Search Status": jaguar.search_status_tag,
        # "Result Actions": jaguar.result_actions_tag_name,
        # RECORD
        # "Index Table": jaguar.index_table_tags,
        # NAVIGATION
        # "Result Button": jaguar.result_button_tag
    }
    abstract.county.other = {
        # DISCLAIMER
        # "Inaccessible": jaguar.inaccessible,
        # RECORD
        # "Missing Values": jaguar.missing_values,
        # "Stock Download": jaguar.stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
