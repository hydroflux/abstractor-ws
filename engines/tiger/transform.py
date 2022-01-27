from settings.county_variables.tiger import stock_download


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = stock_download


def transform_document_list(abstract):
    update_document_attributes(abstract)
