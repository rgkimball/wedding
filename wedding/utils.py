import os
import uuid
import pytz

from .settings import TIME_ZONE

MEALS = [
    ('beef', 'Steak'),
    ('fish', 'Fish'),
    ('vegetarian', 'Vegetarian'),
]


TZ = pytz.timezone(TIME_ZONE)


def _random_uuid():
    return uuid.uuid4().hex


def touch(fname):
    open(fname, 'a').close()
    os.utime(fname, None)
