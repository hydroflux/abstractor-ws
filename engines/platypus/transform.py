import settings.county_variables.platypus as platypus


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = platypus.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": platypus.login_page_url,
        "Home Page": platypus.home_page_url,
        # SEARCH
        "Search Page": platypus.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": platypus.login_page_title,
        "Home Page": platypus.home_page_title,
        # SEARCH
        "Search Page": platypus.search_page_title,
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": platypus.login_button_class_name,
        # SEARCH
        # "Clear Search": platypus.clear_search_id,
        "Search": platypus.search_button_class_name,
        # OPEN DOCUMENT
        "Open Document": platypus.open_document_button_class_name,
        # DOWNLOAD
        "Download Prompt": platypus.download_prompt_id,
        "Download": platypus.download_button_id,
        # LOGOUT
        "Logout Dropdown": platypus.logout_dropdown_button,
        "Logout": platypus.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Redirect Active": platypus.redirect_modal_active_class,
        # OPEN DOCUMENT
        "Result Count Container": platypus.result_count_container_class_name,
        "Result Row": platypus.result_row_class_name,
    }
    abstract.county.ids = {
        "Redirect Modal": platypus.redirect_modal_id,
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        # "Reception Number": platypus.reception_number_input_id,
        # "Book": platypus.book_input_id,
        # "Page": platypus.page_input_id,
        # "Name": platypus.name_input_id,
        # "Start Date": platypus.start_date_id,
        # "End Date": platypus.end_date_id
        "Section": platypus.section_input_id,
        "Township": platypus.township_input_id,
        "Range": platypus.range_input_id
    }
    abstract.county.record = {
        "Document Type": platypus.document_type_class_name,
        "Indexing Information": platypus.indexing_information_id,
        "Parties": platypus.parties_id,
        "Notes": platypus.notes_id,
        "Notes Tag": platypus.notes_tag,
        "Legal": platypus.legal_class_name,
        "Related Documents": platypus.related_documents_class_name
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
