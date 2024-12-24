import settings.county_variables.komodo as komodo


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = komodo.credentials  # LOGIN
    abstract.county.urls = {
        # LOGIN
        "Login Page": komodo.login_page_url,
        # SEARCH
        "Search Page": komodo.search_page_url,
        # COLLECT
        "Search Result Base Url": komodo.search_result_base_url,
        # LOGOUT
        "Logout Page": komodo.logout_page_url
    }
    abstract.county.titles = {
        # LOGIN
        "Login Page": komodo.login_page_title,
        # SEARCH
        "Search Page": komodo.search_page_title,
        # COLLECT
        "Loading": komodo.loading_page_title,
        "Search Results Page": komodo.search_results_page_title,
        # OPEN DOCUMENT
        "Search Result Page": komodo.search_result_page_title,
        # LOGOUT
        "Logout Page": komodo.logout_page_title
    }
    abstract.county.buttons = {
        # LOGIN
        "Login": komodo.login_button_class_name,
        # SEARCH
        "Search": komodo.search_button_class_name,
        # DOWNLOAD
        "Purchase Window": komodo.purchase_window_button_css_selector,
        "Purchase": komodo.purchase_button_css_selector,
        "Download": komodo.download_button_css_selector
    }
    abstract.county.classes = {
        # COLLECT
        "Search Results": komodo.search_results_class_name,
        "Results Per Page Container": komodo.results_per_page_container_class_name,
        "Results Per Page Label": komodo.results_per_page_label_class_name,
        "Results Per Page Button": komodo.results_per_page_button_class_name,
        "Results Per Page Dropdown": komodo.results_per_page_dropdown_class_name,
        "Results Per Page Options": komodo.results_per_page_options_class_name,
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        "Search Input": komodo.search_input_css_selector,
        "Start Date": komodo.start_date_input_css_selector,
        "End Date": komodo.end_date_input_css_selector
    }
    abstract.county.tags = {
        # COLLECT
        "Total Results": komodo.total_search_results_css_selector,
        "Pagination": komodo.pagination_css_selector,
        "Search Results Table": komodo.search_results_table_tag,
        "Reception Number Column": komodo.reception_number_column_css_selector,
        "Result Checkbox": komodo.result_checkbox_css_selector,
        "Next Page": komodo.search_results_next_page_button_css_selector
    }
    abstract.county.record = {
        "Show All Elements": komodo.show_all_elements_class_name,
        "Show Element Text": komodo.show_element_text,
        "Hide Element Text": komodo.hide_element_text,
        "Document Type": komodo.document_type_class_name,
        "Indexing Information": komodo.indexing_information_class_name,
        "Indexing Items": komodo.indexing_items_class_name,
        "Reception Number Text": komodo.reception_number_text,
        "Book Text": komodo.book_text,
        "Page Text": komodo.page_text,
        "Number Pages Text": komodo.number_pages_text,
        "Recording Date Text": komodo.recording_date_text,
        "Additional Information": komodo.parties_related_documents_and_legal_class_name,
        "Parties": komodo.parties_class_name,
        "Party Item Label": komodo.party_item_label_class_name,
        "Party Item Text": komodo.party_item_text_class_name,
        "Grantor Text": komodo.party_item_grantor_text,
        "Grantee Text": komodo.party_item_grantee_text,
        "Related Documents": komodo.related_documents_class_name,
        "No Related Documents": komodo.no_related_documents_text,
        "Related Reception Number": komodo.related_reception_number_class_name,
        "Related Document Type": komodo.related_document_type_class_name,
        "Related Recording Date": komodo.related_recording_date_class_name,
        "No Legal Information Found": komodo.no_legal_information_text,
        "Legal Table": komodo.legal_table_class_name,
        "Legal Table Header": komodo.legal_table_headers_tag_name,
        "Legal Table Body": komodo.legal_table_body_tag_name,
        "Legal Rows": komodo.legal_rows_tag_name,
        "Legal Row Data": komodo.legal_row_data_tag_name,
        "Legal Headers": komodo.legal_item_headers
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
