class County:

    number_counties = 0

    def __init__(self, county_name, prefix, state, state_prefix, engine,
                 credentials=None, cookies=None,
                 urls=None, titles=None, buttons=None, classes=None, ids=None,
                 inputs=None, messages=None, record=None, scripts=None, tags=None,
                 iframes=None, xpaths=None, other=None):
        self.county_name = county_name
        self.prefix = prefix
        self.state = state
        self.state_prefix = state_prefix
        self.engine = engine

        self.credentials = credentials
        self.cookies = cookies

        self.urls = urls
        self.titles = titles
        self.buttons = buttons
        self.classes = classes
        self.ids = ids
        self.inputs = inputs
        self.messages = messages
        self.record = record
        self.scripts = scripts
        self.tags = tags
        self.iframes = iframes
        self.xpaths = xpaths

        # "Other" handles attributes that don't fit into neat categories
        self.other = other

        County.number_counties += 1

    def __str__(self):
        if self.state_prefix == "LA":
            return f'{self.county_name} Parish, {self.state}'
        else:
            return f'{self.county_name} County, {self.state}'

    def shorthand_name(self):
        """
        Returns the full shorthand name of the county.

        This method provides a shorthand representation of the county's name,
        including the county name and state prefix. For counties in Louisiana,
        it uses "Parish" instead of "County".

        Returns:
            str: The shorthand name of the county in the format "{county_name} County, {state_prefix}"
                or "{county_name} Parish, {state_prefix}" for Louisiana.
        """
        if self.state_prefix == "LA":
            return f'{self.county_name} Parish, {self.state_prefix}'
        else:
            return f'{self.county_name} County, {self.state_prefix}'
