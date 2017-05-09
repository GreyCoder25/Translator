letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
digits = set('0123456789')
delimiters = set('.,;\=')
whitespaces = set([chr(9), chr(10), chr(11), chr(12), chr(13), chr(32)])


def is_letter(ch):
    return ch in letters


def is_digit(ch):
    return ch in digits


def is_delimiter(ch):
    return ch in delimiters


def is_whitespace(ch):
    return ch in whitespaces
