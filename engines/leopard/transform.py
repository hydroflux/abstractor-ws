from settings.county_variables.leopard import stock_download


# Identical to the 'tiger' update_document_attributes function
# Similar to the 'jaguar' update_document_attributes function
def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county
        document.download_value = stock_download


# Similar to the 'jaguar' convert_document_numbers function
def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            if year <= 1984:
                document.value = document_number
            else:
                document.value = f'{year}{document_number.zfill(7)}'


# Identical to the 'tiger' transform_document_list function
def transform_document_list(abstract):
    update_document_attributes(abstract)
    convert_document_numbers(abstract)
