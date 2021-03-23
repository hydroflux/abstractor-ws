class County:

    number_counties = 0

    def __init__(self, county_name, county_prefix, state, state_prefix):
        self.county_name = county_name
        self.prefix = county_prefix
        self.state = state
        self.state_prefix = state_prefix

        County.number_counties += 1


    def __str__(self):
        return f'{self.county_name} County, {self.state}'
