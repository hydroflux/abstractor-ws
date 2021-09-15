from armadillo.armadillo_variables import (page_search_field_id,
                                           reception_number_search_field_id,
                                           volume_search_field_id)


def convert_document_numbers(document_list):
    for document in document_list:
        if document.type == 'document_number':
            document.year = document.value[:4]
            document.value = f'{document.year}-{document.value[4:]}'


def update_search_field_ids(document_list):
    for document in document_list:
        document.search_field_ids = {
            "Reception Number": reception_number_search_field_id,
            "Volume": volume_search_field_id,
            "Page": page_search_field_id
            }


def transform_document_list(document_list):
    convert_document_numbers(document_list)
    update_search_field_ids(document_list)
