from project_management.user_prompts import user_profile_selection_prompt
import settings.county_variables.eagle as eagle


def get_user_profile_credentials():
    profile = user_profile_selection_prompt()
    print(f'Executing program using Profile #{profile + 1}:')
    return eagle.credentials[profile]


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = get_user_profile_credentials()
    abstract.county.cookies = eagle.cookies_JSON  # COOKIES
    abstract.county.urls = {
        # LOGIN
        "Home Page": eagle.home_page_url,
        "Fallback Search": eagle.fallback_search_url,
        "Log Out Redirect": eagle.logged_out_redirect_url,
        # SEARCH
        "Search Page": eagle.search_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home Page": eagle.home_page_title,
        # SEARCH
        "Search Page": eagle.search_title,
        # OPEN DOCUMENT
        "Document Description": eagle.document_description_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": eagle.login_button_id,
        # DISCLAIMER
        "Disclaimer": eagle.disclaimer_id,
        # SEARCH
        "Clear Search": eagle.clear_search_id,
        "Submit Search": eagle.search_button_id,
        # DOWNLOAD
        "Download Button": eagle.download_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Login Prompt": eagle.login_prompt_class,
        # OPEN DOCUMENT
        "Validation": eagle.validation_class_name,
        "Results Row": eagle.results_row_class_name,
        "Result Actions": eagle.result_actions_class_name,
        # RECORD
        "Document Table": eagle.document_table_class,
        "Information Links": eagle.information_links_class,
        "Related Documents Table": eagle.related_table_class,
        # DOWNLOAD
        "PDF Viewer": eagle.pdf_viewer_class_name,
        "Purchase Button": eagle.purchase_button_class_name,
        # NAVIGATION
        "Result Buttons": eagle.result_buttons_class,
        # ERROR HANDLING
        "Error Message": eagle.error_message_class
    }
    abstract.county.ids = {
        # LOGIN
        "Username": eagle.user_id,
        "Password": eagle.password_id,
        "Welcome": eagle.welcome_message_id,
        # RECORD
        "Image Container": eagle.image_container_id,
        "Document Information": eagle.document_information_id,
        "PDF Viewer Load Marker": eagle.pdf_viewer_load_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": eagle.reception_number_input_id,
        "Book": eagle.book_input_id,
        "Page": eagle.page_input_id,
        "Name": eagle.name_input_id,
        "Start Date": eagle.start_date_id,
        "End Date": eagle.end_date_id
    }
    abstract.county.messages = {
        # OPEN DOCUMENT
        "Currently Searching": eagle.currently_searching,
        "No Results": eagle.no_results_message,
        "Failed Search": eagle.failed_search,
        "Invalid Search": eagle.invalid_search_message,
        # RECORD
        "No Image Available": eagle.no_image_message,
        "Loading": eagle.loading_status,
        "More Information": eagle.more_info_message,
        "Less Information": eagle.less_info_message,
        "Login Error": eagle.login_error_message,
        # ERROR HANDLING
        "Error Message": eagle.error_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Search Status": eagle.search_status_tag,
        "Result Actions": eagle.result_actions_tag_name,
        # RECORD
        "Index Table": eagle.index_table_tags,
        # NAVIGATION
        "Result Button": eagle.result_button_tag
    }
    abstract.county.other = {
        # DISCLAIMER
        "Inaccessible": eagle.inaccessible,
        "Disclaimer Cookie": eagle.disclaimer_cookie,
        # RECORD
        "Missing Values": eagle.missing_values,
        "Stock Download": eagle.stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
