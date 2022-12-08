import settings.county_variables.buffalo as buffalo


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = buffalo.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Home Page": buffalo.home_page_url,
        # "Fallback Search": buffalo.fallback_search_url,
        # "Log Out Redirect": buffalo.logged_out_redirect_url,
        # SEARCH
        # "Search Page": buffalo.search_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home Page": buffalo.home_page_title,
        "Login": buffalo.post_login_title,
        # SEARCH
        # "Search Page": buffalo.search_title,
        # OPEN DOCUMENT
        # "Document Description": buffalo.document_description_title
    }
    abstract.county.buttons = {
        # LOGIN
        # "Login": buffalo.login_button_id,
        # DISCLAIMER
        "Disclaimer": buffalo.disclaimer_button_id,
        # SEARCH
        "Search Menu": buffalo.search_page_button_id,
        "Document Search Menu": buffalo.document_search_menu_id,
        "Book & Page Search Menu": buffalo.book_and_page_search_menu_id,
        "Search": buffalo.search_button_id,
        # RECORD
        "Related Documents": buffalo.related_documents_button_class_name,
        # "Clear": buffalo.clear_search_id,
        # DOWNLOAD
        "Download Submenu": buffalo.download_submenu_button_id,
        "Download": buffalo.download_button_xpath
    }
    abstract.county.classes = {
        # SEARCH
        "Search Menu Active": buffalo.search_menu_active_class,
        # OPEN DOCUMENT
        "Result Link": buffalo.result_link_class_name
        # RECORD
        # "Validation": buffalo.validation_class_name,
        # "Results Row": buffalo.results_row_class_name,
        # "Result Actions": buffalo.result_actions_class_name,
        # RECORD
        # "Document Table": buffalo.document_table_class,
        # "Information Links": buffalo.information_links_class,
        # "Related Documents Table": buffalo.related_table_class,
        # DOWNLOAD
        # "PDF Viewer": buffalo.pdf_viewer_class_name,
        # "Purchase Button": buffalo.purchase_button_class_name,
        # NAVIGATION
        # "Result Buttons": buffalo.result_buttons_class,
        # ERROR HANDLING
        # "Error Message": buffalo.error_message_class
    }
    abstract.county.ids = {
        # LOGIN
        "Welcome": buffalo.welcome_message_id,
        # OPEN DOCUMENT
        "First Result": buffalo.first_result_id,
        # RECORD
        # "Image Container": buffalo.image_container_id,
        # "Document Information": buffalo.document_information_id,
        # "PDF Viewer Load Marker": buffalo.pdf_viewer_load_id
    }
    abstract.county.iframes = {
        "Main": buffalo.main_frame_name,
        "Header": buffalo.header_frame_name,
        "Search Menu": buffalo.search_menu_frame_name,
        "Search Input": buffalo.search_input_frame_name,
        "Result": buffalo.result_frame_name,
        "Result List": buffalo.result_list_frame_name,
        "Document": buffalo.document_frame_name,
        "Document Information": buffalo.document_information_frame_name,
        "Related Documents Menu": buffalo.related_documents_menu_frame_name,
        "Download Submenu": buffalo.download_submenu_frame_name,
        "Download": buffalo.download_frame_name,
        "Captcha": buffalo.captcha_frame_name
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": buffalo.document_search_field_xpath,
        "Book": buffalo.book_search_field_xpath,
        "Page": buffalo.page_search_field_xpath,
        # "Name": buffalo.name_input_id,
        # "Start Date": buffalo.start_date_id,
        # "End Date": buffalo.end_date_id
    }
    abstract.county.messages = {
        # LOGIN
        "Welcome": buffalo.welcome_message,
        # SEARCH
        "Search Input": buffalo.search_input_header_text,
        # OPEN DOCUMENT
        "Search Results": buffalo.search_results_header_text,
        # RECORD
        "Document Information": buffalo.document_information_header_text,
        "No Related Documents": buffalo.no_related_documents_message
        # "Currently Searching": buffalo.currently_searching,
        # "No Results": buffalo.no_results_message,
        # "Failed Search": buffalo.failed_search,
        # "Invalid Search": buffalo.invalid_search_message,
        # RECORD
        # "No Image Available": buffalo.no_image_message,
        # "Loading": buffalo.loading_status,
        # "More Information": buffalo.more_info_message,
        # "Less Information": buffalo.less_info_message,
        # "Login Error": buffalo.login_error_message,
        # ERROR HANDLING
        # "Error Message": buffalo.error_message
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        # "Search Status": buffalo.search_status_tag,
        # "Result Actions": buffalo.result_actions_tag_name,
        # RECORD
        # "Index Table": buffalo.index_table_tags,
        # NAVIGATION
        # "Result Button": buffalo.result_button_tag
        # VALIDATION
        "Header Text": buffalo.header_text_tag
    }
    abstract.county.scripts = {
        # LOGIN
        "Login": buffalo.login_script,
        "Disclaimer": buffalo.disclaimer_script,
        # LOGOUT
        "Logout": buffalo.logout_script
    }
    abstract.county.xpaths = {
        # RECORD
        "Document Type": buffalo.document_type_xpath,
        "Reception Number": buffalo.reception_number_xpath,
        "Book": buffalo.book_xpath,
        "Page": buffalo.page_xpath,
        "Recording Date": buffalo.recording_date_xpath,
        "Grantor": buffalo.grantor_xpath,
        "Grantee": buffalo.grantee_xpath,
        "Legal": buffalo.legal_xpaths,
        "Related Documents": buffalo.related_documents_xpaths
    }
    abstract.county.other = {
        # DISCLAIMER
        # "Inaccessible": buffalo.inaccessible,
        # RECORD
        # "Missing Values": buffalo.missing_values,
        # "Stock Download": buffalo.stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
