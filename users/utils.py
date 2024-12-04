import string
from random import choices


def create_invite_code():
    """ Рандомная генерация уникального инвайт кода. """
    while True:
        code = ''.join(choices(string.ascii_uppercase + string.digits, k=6))
        return code
