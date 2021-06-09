class Document:
    def __init__(self, type, value, number_results=0, reception_number=None, results=None, year=None):
        self.type = type
        self.value = value
        self.number_results = number_results
        self.reception_number = reception_number
        self.results = results
        self.year = year
