from settings.county_variables.armadillo import (page_input_id,
                                                 reception_number_input_id,
                                                 volume_input_id)


def convert_document_numbers(document_list):
    for document in document_list:
        if document.type == 'document_number' and '-' not in document.value:
            document.year = document.value[:4]
            document.value = f'{document.year}-{document.value[4:]}'


def update_input_ids(document_list):
    for document in document_list:
        document.input_ids = {
            "Reception Number": reception_number_input_id,
            "Volume": volume_input_id,
            "Page": page_input_id
        }


def update_county(document_list, county):
    for document in document_list:
        document.county = county


def transform_document_list(document_list, county):
    convert_document_numbers(document_list)
    update_input_ids(document_list)
    update_county(document_list, county)
