from random import randint
from time import sleep

if __name__ == '__main__':
    import settings.classes.counties as county_data
else:
    from .classes.counties import county_dictionary as county_data


def naptime():
    # sleep(randint(3, 6))
    sleep(randint(2, 3))


def get_county_data(county):
    return county_data.get(county)
