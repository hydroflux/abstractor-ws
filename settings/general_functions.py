from random import randint
from time import sleep

import settings.classes.counties as county_data


def naptime():
    sleep(randint(3, 6))

def get_county_data(county):
    return county_data.county_dictionary.get(county)
