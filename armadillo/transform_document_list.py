def convert_document_numbers(document_list):
    for document in document_list:
        if document.type == 'document_number':
            document.year = document.value[:4]
            document.value = f'{document.year}-{document.value[4:]}'


# Redundant function as it stands, the purpose being to circle back & add additional functionality
def transform_document_list(document_list):
    convert_document_numbers(document_list)
