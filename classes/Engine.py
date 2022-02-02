class Engine:
    def __init__(self, county, name,
                 button_attributes=None, input_attributes=None, search_attributes=None):
        self.county = county
        self.name = name
        self.button_attributes = button_attributes
        self.input_attributes = input_attributes
        self.search_attributes = search_attributes
