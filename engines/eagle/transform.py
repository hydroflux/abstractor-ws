from settings.county_variables.eagle import (book_input_id, clear_search_id, no_results_message,
                                             credentials, download_button_id,
                                             fallback_search_url,
                                             home_page_title, home_page_url, inaccessible, welcome_message,
                                             logged_out_redirect_url, disclaimer_id,
                                             login_button_id, page_input_id, search_url, search_title,
                                             reception_number_input_id, login_prompt_class, document_description_title,
                                             currently_searching, failed_search, invalid_search_message,
                                             search_button_id)


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = credentials
    abstract.county.urls = {
        "Home Page": home_page_url,
        "Fallback Search": fallback_search_url,
        "Log Out Redirect": logged_out_redirect_url,
        "Search Page": search_url
    }
    abstract.county.titles = {
        "Home Page": home_page_title,
        "Search Page": search_title,
        "Document Description": document_description_title
    }
    abstract.county.classes = {
        "Login Prompt": login_prompt_class
    }
    abstract.county.buttons = {
        "Login": login_button_id,
        "Disclaimer": disclaimer_id,
        "Clear Search": clear_search_id,
        "Submit Search": search_button_id,
        "Download Button": download_button_id
    }
    abstract.county.inputs = {
        "Reception Number": reception_number_input_id,
        "Book": book_input_id,
        "Page": page_input_id,
    }
    abstract.county.messages = {
        "Welcome": welcome_message,
        "No Results": no_results_message,
        "Invalid Search": invalid_search_message,
        "Failed Search": failed_search,
        "Currently Searching": currently_searching
    }
    abstract.county.other = {
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
