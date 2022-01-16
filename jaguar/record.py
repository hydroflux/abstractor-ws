from selenium_utilities.locators import locate_element_by_id


from settings.county_variables.jaguar import document_type_and_number_field_id


def access_document_type_and_number(browser, document):
    document_type_and_number_field = locate_element_by_id(browser, document_type_and_number_field_id,
                                                         "document type and number field", document=document)
    return document_type_and_number_field.text.split('\n')[0]


def record_document_type_and_number(browser, dataframe, document):
    document_type_and_number = access_document_type_and_number(browser, document)


def aggregate_document_table_information(browser, dataframe, document):
    pass


def record_comments(dataframe, document):
    pass


def record_document_link(dataframe, document):
    pass


def record(browser, dataframe, document):
    record_document_type_and_number(browser, dataframe, document)
    aggregate_document_table_information(browser, dataframe, document)
