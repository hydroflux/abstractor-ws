from settings.county_variables.eagle import (book_input_id, clear_search_id, no_results_message,
                                             credentials, download_button_id,
                                             fallback_search_url,
                                             home_page_title, home_page_url, inaccessible, welcome_message,
                                             logged_out_redirect_url, disclaimer_id,
                                             login_button_id, page_input_id, search_url, search_title,
                                             reception_number_input_id, login_prompt_class, document_description_title,
                                             currently_searching, failed_search, invalid_search_message,
                                             search_button_id, result_actions_tag_name,
                                             result_actions_class_name,
                                             results_row_class_name,
                                             search_status_tag,
                                             validation_class_name)


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
        # Open Document
        # Record
        # Download
        "Download Button": download_button_id
    }
    abstract.county.classes = {
        # Login
        "Login Prompt": login_prompt_class,
        # Open Document
        "Validation": validation_class_name,
        "Results Row": results_row_class_name,
        "Result Actions": result_actions_class_name
    }
    abstract.county.ids = {

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
        # Open
        "Currently Searching": currently_searching,
        "No Results": no_results_message,
        "Failed Search": failed_search,
        "Invalid Search": invalid_search_message
    }
    abstract.county.tags = {
        # Open Document
        "Search Status": search_status_tag,
        "Result Actions": result_actions_tag_name
    }
    abstract.county.other = {
        # Disclaimer
        "Inaccessible": inaccessible,
    }
    # Create a 'program' or 'engine' class to handle these elements & attributes
    # document.titles = {
    #     "Home Page": home_page_title,

    # }
    # document.urls = {
    #     "Home Page": home_page_url,

    # }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
