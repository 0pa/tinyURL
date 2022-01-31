import re
import random
import string


def format_datetime(datetime):
    """Example: "2017-05-10T20:45:00.000Z","2018-05-16T10:16:24.666Z" """
    return datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'


def is_correct(tiny_url):
    """tiny_url must consist of alphanumeric and underscore symbols"""
    if re.match(r'^[A-Za-z0-9_]{6}$', tiny_url):
        return True
    return False


def generate_tiny_url(length=6):
    """Generates random strings of alphanumeric and underscore symbols
    Args:
        length: the length of output string
    """
    res = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=length))
    return res
