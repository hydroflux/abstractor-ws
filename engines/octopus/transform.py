import settings.county_variables.octopus as octopus


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = octopus.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": octopus.login_page_url,
        "Home Page": octopus.home_page_url,
        # SEARCH
        "Search Page": octopus.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": octopus.login_page_title,
        "Home Page": octopus.home_page_title,
        # SEARCH
        "Search Page": octopus.search_page_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": octopus.login_button_class_name,
        # SEARCH
        # "Clear Search": octopus.clear_search_id,
        "Search": octopus.search_button_class_name,
        # OPEN DOCUMENT
        "Open Document": octopus.open_document_button_class_name,
        # DOWNLOAD
        "Download Prompt": octopus.download_prompt_id,
        "Download": octopus.download_button_id,
        "Cancel Download": octopus.download_cancel_id,
        # LOGOUT
        "Logout Dropdown": octopus.logout_dropdown_button,
        "Logout": octopus.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Redirect Active": octopus.redirect_modal_active_class,
        # OPEN DOCUMENT
        "Result Count Container": octopus.result_count_container_class_name,
        "Result Row": octopus.result_row_class_name
    }
    abstract.county.ids = {
        # LOGIN
        "Redirect Modal": octopus.redirect_modal_id,
        # VALIDATION
        "No Document Image": octopus.no_document_image_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": octopus.reception_number_input_id,
        "Book": octopus.book_input_id,
        "Page": octopus.page_input_id,
        # "Name": octopus.name_input_id,
        # "Start Date": octopus.start_date_id,
        # "End Date": octopus.end_date_id
        "Section": octopus.section_input_id,
        "Township": octopus.township_input_id,
        "Range": octopus.range_input_id
    }
    abstract.county.messages = {
        # VALIDATION
        "No Document Image": octopus.no_document_image_message,
    }
    abstract.county.record = {
        "Document Type": octopus.document_type_class_name,
        "Indexing Information": octopus.indexing_information_id,
        "Parties": octopus.parties_id,
        "Notes": octopus.notes_id,
        "Notes Tag": octopus.notes_tag,
        "Legal": octopus.legal_class_name,
        "Related Documents": octopus.related_documents_class_name
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
