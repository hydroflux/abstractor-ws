class Document:
    def __init__(self, type, value, year=None, number_results=0):
        self.type = type
        self.value = value
        self.year = year
        self.number_results = number_results
