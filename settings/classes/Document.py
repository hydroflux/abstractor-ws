class Document:
    def __init__(self, type, value, number_results=0, index_number=None, reception_number=None,
                 description_link=None, image_link=None, multiple_results=None, year=None,
                 input_ids=None, start_time=None, county=None,
                 download_type=None, download_value=None, download_path=None, new_name=None):
        self.type = type
        self.value = value
        self.number_results = number_results
        self.index_number = index_number
        self.reception_number = reception_number
        self.description_link = description_link
        self.image_link = image_link
        self.multiple_results = multiple_results
        self.year = year
        self.input_ids = input_ids
        self.start_time = start_time
        self.county = county
        self.download_type = download_type
        self.download_value = download_value
        self.download_path = download_path
        self.new_name = new_name

    def document_value(self):
        if self.type == "document_number" or self.type == "name":
            return str(self.value)
        elif self.type == "book_and_page":
            return [str(self.value["Book"]), str(self.value["Page"])]
        elif self.type == "volume_and_page":
            return [str(self.value["Volume"]), str(self.value["Page"])]
        else:
            print('Unable to identify document type while attempting to identify "document value", please review.')
            return None

    def extrapolate_value(self):
        if self.type == "book_and_page":
            return f'Book: {self.value["Book"]}, Page: {self.value["Page"]}'
        elif self.type == "volume_and_page":
            return f'Volume: {self.value["Volume"]}, Page: {self.value["Page"]}'
        elif self.type == "document_number":
            return f'Document number {self.value}'
        elif self.type == "name":
            return f'search name "{self.value}"'
        else:
            print('Unable to identify document type while attempting to "extrapolate document value", please review.')
            return None
