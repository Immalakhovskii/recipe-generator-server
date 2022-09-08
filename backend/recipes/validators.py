from django.core.exceptions import ValidationError


def is_hex_code(value):
    if value[0] != '#':
        raise ValidationError('HEX color code must start with #')
