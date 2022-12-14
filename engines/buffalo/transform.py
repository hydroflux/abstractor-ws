import settings.county_variables.buffalo as buffalo


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = buffalo.credentials
    abstract.county.urls = {
        # LOGIN
        "Home Page": buffalo.home_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home Page": buffalo.home_page_title,
        "Login": buffalo.post_login_title
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": buffalo.disclaimer_button_id,
        # SEARCH
        "Search Menu": buffalo.search_page_button_id,
        "Document Search Menu": buffalo.document_search_menu_id,
        "Book & Page Search Menu": buffalo.book_and_page_search_menu_id,
        "Search": buffalo.search_button_id,
        # RECORD
        "Related Documents": buffalo.related_documents_button_class_name,
        # DOWNLOAD
        "Download Submenu": buffalo.download_submenu_button_id,
        "Download": buffalo.download_button_xpath,
        # NAVIGATION
        "Next Result": buffalo.next_result_button_id
    }
    abstract.county.classes = {
        # SEARCH
        "Search Menu Active": buffalo.search_menu_active_class,
        # OPEN DOCUMENT
        "Result Link": buffalo.result_link_class_name,
        "Visited Result Link": buffalo.visited_result_link_class_name
    }
    abstract.county.ids = {
        # LOGIN
        "Welcome": buffalo.welcome_message_id,
        # OPEN DOCUMENT
        "First Result Link": buffalo.first_result_link_id,
        "Book And Page First Result": buffalo.book_and_page_first_result_xpath,
        # VALIDATION
        "No Results": buffalo.no_results_id,
        "No Document Image": buffalo.no_document_image_id
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
        "Document Image": buffalo.document_image_frame_name,
        "Download Submenu": buffalo.download_submenu_frame_name,
        "Download": buffalo.download_frame_name,
        "Captcha": buffalo.captcha_frame_name
    }
    abstract.county.inputs = {
        # SEARCH
        "Reception Number": buffalo.document_search_field_xpath,
        "Book": buffalo.book_search_field_xpath,
        "Page": buffalo.page_search_field_xpath
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
        "No Related Documents": buffalo.no_related_documents_message,
        # VALIDATION
        "No Results": buffalo.no_results_message,
        "No Document Image": buffalo.no_document_image_message,
        "No Document Image Alert": buffalo.no_document_image_alert
    }
    abstract.county.tags = {
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


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
