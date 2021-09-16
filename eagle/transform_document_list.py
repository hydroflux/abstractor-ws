def update_county(document_list, county):
    for document in document_list:
        document.county = county


def transform_document_list(document_list, county):
    update_county(document_list, county)
