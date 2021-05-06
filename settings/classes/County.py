class County:

    number_counties = 0

    def __init__(self, county_name, prefix, state, state_prefix, program):
        self.county_name = county_name
        self.prefix = prefix
        self.state = state
        self.state_prefix = state_prefix
        self.program = program

        County.number_counties += 1

    def __str__(self):
        return f'{self.county_name} County, {self.state}'
