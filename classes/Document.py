class Document:
    def __init__(self, type, value, year=None, index_number=None,
                 number_results=0, multiple_results=None, result_number=0, reception_number=None,
                 description_link=None, image_available=True, image_link=None,
                 button_attributes=None, input_attributes=None, search_attributes=None,
                 county=None, start_time=None,
                 download_type=None, download_value=None, download_path=None, new_name=None):
        self.type = type
        self.value = value
        self.year = year
        self.index_number = index_number
        self.number_results = number_results
        self.multiple_results = multiple_results
        self.result_number = result_number
        self.reception_number = reception_number
        self.description_link = description_link
        self.image_available = image_available
        self.image_link = image_link
        self.button_attributes = button_attributes
        self.input_attributes = input_attributes
        self.search_attributes = search_attributes
        self.county = county
        self.start_time = start_time
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
