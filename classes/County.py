class County:

    number_counties = 0

    def __init__(self, county_name, prefix, state, state_prefix, engine,
                 credentials=None, urls=None, titles=None,
                 buttons=None, classes=None, ids=None, inputs=None,
                 messages=None, scripts=None, tags=None, other=None):
        self.county_name = county_name
        self.prefix = prefix
        self.state = state
        self.state_prefix = state_prefix
        self.engine = engine

        self.credentials = credentials

        self.urls = urls
        self.titles = titles
        self.buttons = buttons
        self.classes = classes
        self.ids = ids
        self.inputs = inputs
        self.messages = messages
        self.scripts = scripts
        self.tags = tags

        # "Other" handles attributes that don't fit into neat categories
        self.other = other

        County.number_counties += 1

    def __str__(self):
        if self.state_prefix == "LA":
            return f'{self.county_name} Parish, {self.state}'
        else:
            return f'{self.county_name} County, {self.state}'
