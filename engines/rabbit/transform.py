import settings.county_variables.rabbit as rabbit


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = rabbit.stock_download


def update_county_attributes(abstract):
    abstract.county.urls = {
        # LOGIN
        "Home": rabbit.home_page_url,
        # SEARCH
        "Document Search": rabbit.document_search_url,
        # NAME SEARCH
        "Name Search": rabbit.name_search_url
    }
    abstract.county.titles = {
        # LOGIN
        "Home": rabbit.home_page_title,
        # SEARCH
        "Document Search": rabbit.document_search_title,
        # NAME SEARCH
        "Name Search": rabbit.name_search_title,
        # OPEN DOCUMENT
        "Row Titles": rabbit.row_titles
    }
    abstract.county.buttons = {
        # DISCLAIMER
        "Disclaimer": rabbit.disclaimer_button_id,
        # SEARCH
        "Document Search": rabbit.document_search_button_id,
        # NAME SEARCH
        "Name Search": rabbit.name_search_button_id,
        # DOWNLOAD
        "Download Submenu": rabbit.download_submenu_id,
        "Download": rabbit.download_button_id
    }
    abstract.county.classes = {
        # DISCLAIMER
        "Disclaimer Active": rabbit.disclaimer_active_class,
    }
    abstract.county.ids = {
        # DISCLAIMER
        'Disclaimer': rabbit.disclaimer_id,
        # SEARCH
        "Search Navigation": rabbit.search_navigation_id,
        "Document Search Tab": rabbit.document_search_tab_id,
        # NAME SEARCH
        "Name Search Tab": rabbit.name_search_tab_id,
        # OPEN DOCUMENT
        "Result Count": rabbit.results_count_id,
        "Results Table": rabbit.results_table_id,
        # RECORD
        "Document Image": rabbit.document_image_id,
        "Document Information": rabbit.document_information_id
    }
    abstract.county.inputs = {
        # SEARCH
        "Reception Number": rabbit.document_search_field_id,
        # NAME SEARCH
        "Name": rabbit.name_search_field_id,
        "Start Date": rabbit.name_search_start_date_field_id,
        "End Date": rabbit.name_search_end_date_field_id
    }
    abstract.county.tags = {
        # OPEN DOCUMENT
        "Table Body": rabbit.table_body_tag,
        "Rows": rabbit.row_tag,
        "Data": rabbit.cell_tag,
    }
    abstract.county.scripts = {
        # DISCLAIMER
        "Open Search": rabbit.open_script
    }
    abstract.county.other = {
        "Abbreviation": rabbit.book_page_abbreviation
    }


def transform(abstract):
    update_document_attributes(abstract)
    update_county_attributes(abstract)
