import random
import string

from django.db import connection, reset_queries


def generate_random_string(max_length: int = 254) ->  str:
    return ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase, k=random.randint(1, max_length),
    ))

def generate_random_typed_value(data_type):
    if data_type == 'float':
        return round(random.uniform(-100000, 100000), 5)
    elif data_type == 'int':
        return random.randint(-100000, 100000)
    else:
        return generate_random_string(254)