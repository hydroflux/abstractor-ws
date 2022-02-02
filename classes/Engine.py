class Engine:
    def __init__(self, name, county,
                 button_attributes=None, input_attributes=None, search_attributes=None):
        self.name = name
        self.county = county
        self.button_attributes = button_attributes
        self.input_attributes = input_attributes
        self.search_attributes = search_attributes
