from settings.county_variables.jaguar import (name_input_id,
                                              reception_number_input_id,
                                              search_button_name)


def update_county(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            document.year = int(year)
            document.value = f'{year}{document_number.zfill(6)}'


def update_element_attributes(abstract):
    for document in abstract.document_list:
        document.input_attributes = {
            "Reception Number": reception_number_input_id,
            "Name": name_input_id
        }
        document.button_attributes = {
            "Submit Search": search_button_name
        }


def transform_document_list(abstract):
    update_county(abstract)
    convert_document_numbers(abstract)
    update_element_attributes(abstract)
