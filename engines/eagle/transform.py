import settings.county_variables.eagle as eagle


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = eagle.credentials  # Login
    abstract.county.urls = {
        # Login
        "Home Page": eagle.home_page_url,
        "Fallback Search": eagle.fallback_search_url,
        "Log Out Redirect": eagle.logged_out_redirect_url,
        # Search
        "Search Page": eagle.search_url
    }
    abstract.county.titles = {
        # Login
        "Home Page": eagle.home_page_title,
        # Search
        "Search Page": eagle.search_title,
        # Document Description
        "Document Description": eagle.document_description_title
    }
    abstract.county.buttons = {
        # Login
        "Login": eagle.login_button_id,
        # Disclaimer
        "Disclaimer": eagle.disclaimer_id,
        # Search
        "Clear Search": eagle.clear_search_id,
        "Submit Search": eagle.search_button_id,
        # Download
        "Download Button": eagle.download_button_id
    }
    abstract.county.classes = {
        # Login
        "Login Prompt": eagle.login_prompt_class,
        # Open Document
        "Validation": eagle.validation_class_name,
        "Results Row": eagle.results_row_class_name,
        "Result Actions": eagle.result_actions_class_name,
        # Record
        "Document Table": eagle.document_table_class,
        "Information Links": eagle.information_links_class,
        "Related Documents Table": eagle.related_table_class,
        "Result Buttons": eagle.result_buttons_class,
        # Download
        "PDF Viewer": eagle.pdf_viewer_class_name,
        "Purchase Button": eagle.purchase_button_class_name,
        # Error Handling
        "Error Message": eagle.error_message_class
    }
    abstract.county.ids = {
        # Record
        "Image Container": eagle.image_container_id,
        "Document Information": eagle.document_information_id,
        "PDF Viewer Load Marker": eagle.pdf_viewer_load_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # Search
        "Reception Number": eagle.reception_number_input_id,
        "Book": eagle.book_input_id,
        "Page": eagle.page_input_id,
    }
    abstract.county.messages = {
        # Login
        "Welcome": eagle.welcome_message,  # Not used
        # Open Document
        "Currently Searching": eagle.currently_searching,
        "No Results": eagle.no_results_message,
        "Failed Search": eagle.failed_search,
        "Invalid Search": eagle.invalid_search_message,
        # Record
        "No Image Available": eagle.no_image_message,
        "Loading": eagle.loading_status,
        "More Information": eagle.more_info_message,
        "Less Information": eagle.less_info_message,
        "Login Error": eagle.login_error_message,
        # Error Handling
        "Error Message": eagle.error_message
    }
    abstract.county.tags = {
        # Open Document
        "Search Status": eagle.search_status_tag,
        "Result Actions": eagle.result_actions_tag_name,
        # Record
        "Index Table": eagle.index_table_tags,
        "Result Button": eagle.result_button_tag
    }
    abstract.county.other = {
        # Disclaimer
        "Inaccessible": eagle.inaccessible,
        # Record
        "Missing Values": eagle.missing_values,
        "Stock Download": eagle.stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
