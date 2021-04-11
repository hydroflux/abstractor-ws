def convert_document_numbers(document_list):
    for document in document_list:
        if document.type == "document_number":
            doc_number, year = document.split('-')
            year = int(year)
            if year <= 1984:
                new_name = doc_number
            elif int(doc_number) <= 9:
                new_name = ('{}000000{}'.format(year, doc_number))
            elif int(doc_number) <= 99:
                new_name = ('{}00000{}'.format(year, doc_number))
            elif int(doc_number) <= 999:
                new_name = ('{}0000{}'.format(year, doc_number))
            elif int(doc_number) <= 9999:
                new_name = ('{}000{}'.format(year, doc_number))
            elif int(doc_number) <= 99999:
                new_name = ('{}00{}'.format(year, doc_number))
            elif int(doc_number) <= 999999:
                new_name = ('{}0{}'.format(year, doc_number))
            else:
                new_name = ('{}{}'.format(year, doc_number))
                print(new_name)
            document.value = new_name
