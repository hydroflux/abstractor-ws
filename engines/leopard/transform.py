def convert_document_numbers(abstract):
    for document in abstract.document_list:
        if document.type == "document_number" and document.value.find("-") != -1:
            document_number, year = document.value.split("-")
            year = int(year)
            if year <= 1984:
                new_name = document_number
            elif int(document_number) <= 9:
                new_name = ('{}000000{}'.format(year, document_number))
            elif int(document_number) <= 99:
                new_name = ('{}00000{}'.format(year, document_number))
            elif int(document_number) <= 999:
                new_name = ('{}0000{}'.format(year, document_number))
            elif int(document_number) <= 9999:
                new_name = ('{}000{}'.format(year, document_number))
            elif int(document_number) <= 99999:
                new_name = ('{}00{}'.format(year, document_number))
            elif int(document_number) <= 999999:
                new_name = ('{}0{}'.format(year, document_number))
            else:
                new_name = ('{}{}'.format(year, document_number))
            document.value = new_name
            document.year = year


# Redundant function as it stands, the purpose being to circle back & add additional functionality
def transform_document_list(abstract):
    convert_document_numbers(abstract)
