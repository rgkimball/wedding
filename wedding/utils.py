import uuid


MEALS = [
    ('beef', 'Steak'),
    ('fish', 'Fish'),
    ('vegetarian', 'Vegetarian'),
]

def _random_uuid():
    return uuid.uuid4().hex