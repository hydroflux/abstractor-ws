import settings.county_variables.swordfish as swordfish


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = swordfish.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": swordfish.login_page_url,
        "Home Page": swordfish.home_page_url,
        # SEARCH
        "Search Page": swordfish.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": swordfish.login_page_title,
        "Home Page": swordfish.home_page_title,
        # SEARCH
        "Search Page": swordfish.search_page_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": swordfish.login_button_class_name,
        # SEARCH
        "Search": swordfish.search_button_class_name,
        # OPEN DOCUMENT
        "Open Document": swordfish.open_document_button_class_name,
        # DOWNLOAD
        "Download Prompt": swordfish.download_prompt_id,
        "Download": swordfish.download_button_id,
        "Cancel Download": swordfish.download_cancel_id,
        # LOGOUT
        "Logout Dropdown": swordfish.logout_dropdown_button,
        "Logout": swordfish.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Redirect Active": swordfish.redirect_modal_active_class,
        # OPEN DOCUMENT
        "Result Count Container": swordfish.result_count_container_class_name,
        "Result Row": swordfish.result_row_class_name
    }
    abstract.county.ids = {
        # LOGIN
        "Redirect Modal": swordfish.redirect_modal_id,
        # VALIDATION
        "No Document Image": swordfish.no_document_image_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": swordfish.reception_number_input_id,
        "Book": swordfish.book_input_id,
        "Page": swordfish.page_input_id,
        # "Name": swordfish.name_input_id,
        # "Start Date": swordfish.start_date_id,
        # "End Date": swordfish.end_date_id
        "Section": swordfish.section_input_id,
        "Township": swordfish.township_input_id,
        "Range": swordfish.range_input_id
    }
    abstract.county.messages = {
        # VALIDATION
        "No Document Image": swordfish.no_document_image_message
    }
    abstract.county.record = {
        "Document Type": swordfish.document_type_class_name,
        "Indexing Information": swordfish.indexing_information_id,
        "Parties": swordfish.parties_id,
        "Notes": swordfish.notes_id,
        "Notes Tag": swordfish.notes_tag,
        "Legal": swordfish.legal_class_name,
        "Related Documents": swordfish.related_documents_class_name
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
