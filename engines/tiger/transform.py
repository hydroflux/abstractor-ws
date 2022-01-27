from settings.county_variables.tiger import stock_download


# Identical to the 'leopard' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = stock_download


def convert_document_numbers(abstract):
    # Use the leopard 'transform' script as a model
    pass


def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
