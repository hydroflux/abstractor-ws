import settings.county_variables.armadillo as armadillo


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = armadillo.credentials  # LOGIN
    abstract.county.cookies = armadillo.cookies_JSON  # COOKIES
    abstract.county.urls = {
        # LOGIN
        "Home Page": armadillo.home_page_url,
        # SEARCH
        "Search Page": armadillo.search_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home Page": armadillo.home_page_title,
        # SEARCH
        "Search Page": armadillo.search_title,
        # OPEN DOCUMENT
        "Document Description": armadillo.document_description_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": armadillo.login_button_id,
        # DISCLAIMER
        "Disclaimer": armadillo.disclaimer_id,
        # SEARCH
        "Clear Search": armadillo.clear_search_button_id,
        "Submit Search": armadillo.search_button_id,
        # DOWNLOAD
        "Download Button": armadillo.download_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Login Prompt": armadillo.login_prompt_class_name,
        # OPEN DOCUMENT
        "Validation": armadillo.validation_class_name,
        "Results Row": armadillo.results_row_class_name,
        "Result Actions": armadillo.result_actions_class_name,
        # RECORD
        "Document Table": armadillo.document_table_class,
        "Information Links": armadillo.information_links_class,
        "Related Documents Table": armadillo.related_table_class,
        # NAVIGATION
        "Result Buttons": armadillo.result_buttons_class,
        # DOWNLOAD
        "PDF Viewer": armadillo.pdf_viewer_class_name,
        "Purchase Button": armadillo.purchase_button_class_name,
        # ERROR HANDLING
        "Error Message": armadillo.error_message_class
    }
    abstract.county.ids = {
        # LOGIN
        "Username": armadillo.username_input_id,
        "Password": armadillo.password_input_id,
        "Welcome": armadillo.welcome_message_id,
        # RECORD
        "Image Container": armadillo.image_container_id,
        "Document Information": armadillo.document_information_id,
        "PDF Viewer Load Marker": armadillo.pdf_viewer_load_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": armadillo.reception_number_input_id,
        "Book": armadillo.book_input_id,
        "Volume": armadillo.volume_input_id,
        "Page": armadillo.page_input_id,
        "Name": armadillo.name_input_id,
        "Start Date": armadillo.start_date_input_id,
        "End Date": armadillo.end_date_input_id
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Currently Searching": armadillo.currently_searching_message,
        "No Results": armadillo.no_results_message,
        "Failed Search": armadillo.failed_search_message,
        "Invalid Search": armadillo.invalid_search_message,
        # RECORD
        "No Image Available": armadillo.no_image_message,
        "Loading": armadillo.loading_status,
        "More Information": armadillo.more_info_message,
        "Less Information": armadillo.less_info_message,
        "Login Error": armadillo.login_error_message,
        # ERROR HANDLING
        "Error Message": armadillo.error_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Search Status": armadillo.search_status_tag,
        "Result Actions": armadillo.result_actions_tag_name,
        # RECORD
        "Index Table": armadillo.index_table_tags,
        # NAVIGATION
        "Result Button": armadillo.result_button_tag
    }
    abstract.county.other = {
        # DISCLAIMER
        "Inaccessible": armadillo.inaccessible,
        # RECORD
        "Missing Values": armadillo.missing_values,
        "Stock Download": armadillo.stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
