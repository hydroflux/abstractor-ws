from settings.county_variables.eagle import (book_input_id, clear_search_id,
                                             credentials, currently_searching,
                                             disclaimer_id,
                                             document_description_title,
                                             document_information_id,
                                             document_table_class,
                                             download_button_id, error_message,
                                             error_message_class,
                                             failed_search,
                                             fallback_search_url,
                                             home_page_title, home_page_url,
                                             image_container_id, inaccessible,
                                             index_table_tags,
                                             information_links_class,
                                             invalid_search_message,
                                             less_info_message, loading_status,
                                             logged_out_redirect_url,
                                             login_button_id,
                                             login_error_message,
                                             login_prompt_class,
                                             missing_values, more_info_message,
                                             no_image_message,
                                             no_results_message, page_input_id,
                                             pdf_viewer_load_id,
                                             reception_number_input_id,
                                             related_table_class,
                                             result_actions_class_name,
                                             result_actions_tag_name,
                                             result_button_tag,
                                             result_buttons_class,
                                             results_row_class_name,
                                             search_button_id,
                                             search_status_tag, search_title,
                                             search_url, stock_download_suffix,
                                             validation_class_name,
                                             welcome_message)


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = credentials  # Login
    abstract.county.urls = {
        # Login
        "Home Page": home_page_url,
        "Fallback Search": fallback_search_url,
        "Log Out Redirect": logged_out_redirect_url,
        # Search
        "Search Page": search_url
    }
    abstract.county.titles = {
        # Login
        "Home Page": home_page_title,
        # Search
        "Search Page": search_title,
        # Document Description
        "Document Description": document_description_title
    }
    abstract.county.buttons = {
        # Login
        "Login": login_button_id,
        # Disclaimer
        "Disclaimer": disclaimer_id,
        # Search
        "Clear Search": clear_search_id,
        "Submit Search": search_button_id,
        # Download
        "Download Button": download_button_id
    }
    abstract.county.classes = {
        # Login
        "Login Prompt": login_prompt_class,
        # Open Document
        "Validation": validation_class_name,
        "Results Row": results_row_class_name,
        "Result Actions": result_actions_class_name,
        # Record
        "Document Table": document_table_class,
        "Information Links": information_links_class,
        "Related Documents Table": related_table_class,
        "Result Buttons": result_buttons_class,
        "Error Message": error_message_class
    }
    abstract.county.ids = {
        # Record
        "Image Container": image_container_id,
        "Document Information": document_information_id,
        "PDF Viewer": pdf_viewer_load_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # Search
        "Reception Number": reception_number_input_id,
        "Book": book_input_id,
        "Page": page_input_id,
    }
    abstract.county.messages = {
        # Login
        "Welcome": welcome_message,  # Not used
        # Open Document
        "Currently Searching": currently_searching,
        "No Results": no_results_message,
        "Failed Search": failed_search,
        "Invalid Search": invalid_search_message,
        # Record
        "No Image Available": no_image_message,
        "Loading": loading_status,
        "More Information": more_info_message,
        "Less Information": less_info_message,
        "Error Message": error_message,
        "Login Error": login_error_message
    }
    abstract.county.tags = {
        # Open Document
        "Search Status": search_status_tag,
        "Result Actions": result_actions_tag_name,
        # Record
        "Index Table": index_table_tags,
        "Result Button": result_button_tag
    }
    abstract.county.other = {
        # Disclaimer
        "Inaccessible": inaccessible,
        # Record
        "Missing Values": missing_values,
        "Stock Download": stock_download_suffix
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
