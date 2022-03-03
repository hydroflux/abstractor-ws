from datetime import datetime

import settings.county_variables.mountain_lion as mountain_lion


def convert_document_numbers(abstract):
    for row in abstract.document_list:
        # Reception numbers prior to 1990 start with the letter "R"
        # Reception numbers between 01/01/1990 and 10/31/1995 start with the last two digits of the year
        y_start = datetime.strptime('1990-01-01', '%Y-%m-%d')
        # Reception numbers between 11/01/1995 and 12/31/1999 start with the letter "A"
        a_start = datetime.strptime('1995-11-01', '%Y-%m-%d')
        # Reception numbers between 01/01/2000 and 12/31/2009 start with the letter "B"
        b_start = datetime.strptime('2000-01-01', '%Y-%m-%d')
        # Reception numbers after 12/31/2009 "D"
        d_start = datetime.strptime('2009-12-31', '%Y-%m-%d')
        # Reception numbers after 12/31/2019 "E"
        e_start = datetime.strptime('2019-12-31', '%Y-%m-%d')
        #####################################################
        # IDENTIFY NUMBER, LENGTH, AND DATE #########
        number = row['Instrument_Number'][:-5]
        length = len(number)
        # print(row['Recording_Date'])
        # print(row['Recording_Date'] > d_start)
        # DETERMINE RECEPTION NUMBER CODE FOR NEW DOCUMENT NUMBER
        if row['Recording_Date'] < y_start:
            return 'R' + number
        elif row['Recording_Date'] >= y_start and row['Recording_Date'] < a_start:
            year = row['Instrument_Number'][-2:]
            if length < 6:
                return year + number.zfill(6)
            elif length == 6:
                return year + number
        elif row['Recording_Date'] >= a_start and row['Recording_Date'] < b_start:
            year = row['Instrument_Number'][-1:]
            code = 'A'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= b_start and row['Recording_Date'] < d_start:
            year = row['Instrument_Number'][-1:]
            code = 'B'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= d_start and row['Recording_Date'] < e_start:
            year = row['Instrument_Number'][-1:]
            code = 'D'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= e_start:
            year = row['Instrument_Number'][-1:]
            code = 'E'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        else:
            return 'Other'


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    abstract.county.credentials = mountain_lion.credentials
    abstract.county.urls = {
        # LOGIN
        'Login': mountain_lion.login_url,
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.titles = {
        # LOGIN
        'Login': mountain_lion.login_title,
        'Post Login': mountain_lion.post_login_title,
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.buttons = {
        # SEARCH
        'Open Search': mountain_lion.open_search_page_button_id,
        'Document Search Menu': mountain_lion.document_search_menu_button_id,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.classes = {
        # SEARCH
        'Active': mountain_lion.search_menu_active_class
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.ids = {
        # LOGIN
        'Post Login': mountain_lion.post_login_message_id,
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.inputs = {  # Consider changing to 'search_inputs'
        # SEARCH
        'Reception Number': mountain_lion.document_search_field_class_name
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.messages = {
        # LOGIN
        'Post Login': mountain_lion.post_login_message,
        # SEARCH
        'Search Header': mountain_lion.header_search_message,
        # OPEN DOCUMENT
        'Results Header': mountain_lion.header_results_message,
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }
    abstract.county.scripts = {
        # LOGIN
        'Login': mountain_lion.login_script,
        # DISCLAIMER
        'Disclaimer': mountain_lion.disclaimer_script,
        # SEARCH
        'Search': mountain_lion.document_search_script,
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
        'Logout': mountain_lion.logout_script
    }
    abstract.county.tags = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
        # VALIDATION
        'Header Text': mountain_lion.header_text_tag
    }
    abstract.county.iframes = {
        'Main': mountain_lion.main_frame_name,
        'Header': mountain_lion.header_frame_name,
        'Search Menu': mountain_lion.search_menu_frame_name,
        'Search Input': mountain_lion.search_input_frame_name,
        'Search Results': mountain_lion.result_frame_name,
        'Search Results List': mountain_lion.result_list_frame_name
    }
    abstract.county.other = {
        # SEARCH
        # OPEN DOCUMENT
        # RECORD
        # DOWNLOAD
        # LOGOUT
    }


def transform(abstract):
    convert_document_numbers(abstract)
    update_document_attributes(abstract)
    update_county_attributes(abstract)
