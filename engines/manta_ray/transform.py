import settings.county_variables.manta_ray as manta_ray


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = manta_ray.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": manta_ray.login_page_url,
        "Home Page": manta_ray.home_page_url,
        # SEARCH
        "Search Page": manta_ray.search_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": manta_ray.login_page_title,
        "Home Page": manta_ray.home_page_title,
        # SEARCH
        "Search Page": manta_ray.search_page_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": manta_ray.login_button_class_name,
        # SEARCH
        "Search": manta_ray.search_button_class_name,
        # OPEN DOCUMENT
        "Open Document": manta_ray.open_document_button_class_name,
        # DOWNLOAD
        "Download Prompt": manta_ray.download_prompt_id,
        "Download": manta_ray.download_button_id,
        "Cancel Download": manta_ray.download_cancel_id,
        # LOGOUT
        "Logout Dropdown": manta_ray.logout_dropdown_button,
        "Logout": manta_ray.logout_button_id
    }
    abstract.county.classes = {
        # LOGIN
        "Redirect Active": manta_ray.redirect_modal_active_class,
        # PAGE COUNT
        "Page Count": manta_ray.page_count_container_class,
        # OPEN DOCUMENT
        "Result Count Container": manta_ray.result_count_container_class_name,
        "Result Row": manta_ray.result_row_class_name
    }
    abstract.county.ids = {
        # LOGIN
        "Redirect Modal": manta_ray.redirect_modal_id,
        # VALIDATION
        "No Document Image": manta_ray.no_document_image_id
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Reception Number": manta_ray.reception_number_input_id,
        "Book": manta_ray.book_input_id,
        "Page": manta_ray.page_input_id,
        "Section": manta_ray.section_input_id,
        "Township": manta_ray.township_input_id,
        "Range": manta_ray.range_input_id
    }
    abstract.county.tags = {
        # PAGE COUNT
        "Page Count": manta_ray.page_count_element_tag
    }
    abstract.county.messages = {
        # VALIDATION
        "No Document Image": manta_ray.no_document_image_message
    }
    abstract.county.record = {
        "Document Type": manta_ray.document_type_class_name,
        "Indexing Information": manta_ray.indexing_information_id,
        "Parties": manta_ray.parties_id,
        "Notes": manta_ray.notes_id,
        "Notes Tag": manta_ray.notes_tag,
        "Legal": manta_ray.legal_class_name,
        "Related Documents": manta_ray.related_documents_class_name
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
