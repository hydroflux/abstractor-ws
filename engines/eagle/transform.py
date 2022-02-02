from settings.county_variables.eagle import (credentials, book_input_id, clear_search_id, login_button_id,
                                             download_button_id, page_input_id,
                                             reception_number_input_id,
                                             search_button_id)


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = credentials
    abstract.county.urls = {

    }
    abstract.county.buttons = {
            "Login": login_button_id,
            "Clear Search": clear_search_id,
            "Submit Search": search_button_id,
            "Download Button": download_button_id
    }
    abstract.county.inputs = {
            "Reception Number": reception_number_input_id,
            "Book": book_input_id,
            "Page": page_input_id,
        }
    abstract.county.searches = {

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
