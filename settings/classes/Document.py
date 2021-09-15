class Document:
    def __init__(self, type, value, number_results=0, index_number=None, reception_number=None,
                 description_link=None, image_link=None, multiple_results=None, year=None, download_type=None,
                 search_field_ids=None):
        self.type = type
        self.value = value
        self.number_results = number_results
        self.index_number = index_number
        self.reception_number = reception_number
        self.description_link = description_link
        self.image_link = image_link
        self.multiple_results = multiple_results
        self.year = year
        self.download_type = download_type
        self.search_field_ids = search_field_ids
