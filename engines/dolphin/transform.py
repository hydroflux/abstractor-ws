import settings.county_variables.dolphin as dolphin


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = dolphin.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": dolphin.login_page_url,
        "Home Page": dolphin.home_page_url,
        # SEARCH
        "Search Page": dolphin.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": dolphin.login_page_title,
        "Home Page": dolphin.home_page_title,
        # SEARCH
        "Search Page": dolphin.search_page_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": dolphin.login_button_class_name,
        # SEARCH
        "Search": dolphin.search_button_class_name,
        # OPEN DOCUMENT
        "Open Document": dolphin.open_document_button_class_name,
        # DOWNLOAD
        "Download Prompt": dolphin.download_prompt_id,
        "Download": dolphin.download_button_id,
        "Cancel Download": dolphin.download_cancel_id,
        # LOGOUT
        "Logout Dropdown": dolphin.logout_dropdown_button,
        "Logout": dolphin.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Redirect Active": dolphin.redirect_modal_active_class,
        # OPEN DOCUMENT
        "Result Count Container": dolphin.result_count_container_class_name,
        "Result Row": dolphin.result_row_class_name
    }
    abstract.county.ids = {
        # LOGIN
        "Redirect Modal": dolphin.redirect_modal_id,
        # VALIDATION
        "No Document Image": dolphin.no_document_image_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": dolphin.reception_number_input_id,
        "Book": dolphin.book_input_id,
        "Page": dolphin.page_input_id,
        # "Name": dolphin.name_input_id,
        # "Start Date": dolphin.start_date_id,
        # "End Date": dolphin.end_date_id
        "Section": dolphin.section_input_id,
        "Township": dolphin.township_input_id,
        "Range": dolphin.range_input_id
    }
    abstract.county.messages = {
        # VALIDATION
        "No Document Image": dolphin.no_document_image_message
    }
    abstract.county.record = {
        "Document Type": dolphin.document_type_class_name,
        "Indexing Information": dolphin.indexing_information_id,
        "Parties": dolphin.parties_id,
        "Notes": dolphin.notes_id,
        "Notes Tag": dolphin.notes_tag,
        "Legal": dolphin.legal_class_name,
        "Related Documents": dolphin.related_documents_class_name
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
