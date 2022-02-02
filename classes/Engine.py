class Engine:
    def __init__(self, county, name=None,
                 button_attributes=None, input_attributes=None, search_attributes=None):
        self.county = county
        self.name = name
        self.button_attributes = button_attributes
        self.input_attributes = input_attributes
        self.search_attributes = search_attributes

# name=None until Engine and County class conflicts are updated
