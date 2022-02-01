from datetime import datetime
from random import randint
from time import sleep

# Timeout / Wait Variables
timeout = randint(20, 30)
long_timeout = randint(120, 180)
short_timeout = randint(5, 10)


def naptime():
    sleep(randint(3, 4))  # Consider adding an additional second if running into issues while using naps


def micro_nap():
    if randint(0, 1) == 0:
        sleep(0.25)
    else:
        sleep(0.5)


def short_nap():
    sleep(randint(1, 2))


def medium_nap():
    sleep(randint(10, 20))


def long_nap():
    sleep(randint(30, 45))


def start_timer():
    return datetime.now()


def stop_timer(start_time):
    return datetime.now() - start_time
