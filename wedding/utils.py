import os
import random
import pytz
from datetime import datetime as dt, timedelta as td

from .settings import TIME_ZONE, BASE_DIR, SESSION_COOKIE_AGE, SESSION_COOKIE_DOMAIN

MEALS = [
    ('beef', 'Steak'),
    ('fish', 'Fish'),
    ('vegetarian', 'Vegetarian'),
]


TZ = pytz.timezone(TIME_ZONE)


def _random_uuid():
    fp = os.path.join(BASE_DIR, 'wedding', 'words.txt')
    with open(fp, 'r') as fo:
        lines = fo.read().splitlines()

    login_id = '-'.join(random.choices(lines, k=3))

    return login_id


def touch(fname):
    open(fname, 'a').close()
    os.utime(fname, None)


def set_cookie(response, key, value):
    expires = dt.strftime(dt.utcnow() + td(seconds=SESSION_COOKIE_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        key, value,
        max_age=SESSION_COOKIE_AGE,
        expires=expires,
        domain=SESSION_COOKIE_DOMAIN,
        secure=True,
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)