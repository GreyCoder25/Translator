ident_table = {}
ident_code = 1001

const_table = {}
const_code = 501

key_words_table = {'PROGRAM': 401, 'BEGIN': 402, 'END': 403, 'DEFFUNC': 404, 'SIN': 405}
key_word_code = 405

def in_ident_table(word):
    return word in ident_table


def in_const_table(num):
    return num in const_table


def in_key_words_table(word):
    return word in key_words_table


def add_to_ident_table(word):
    global ident_code
    ident_table[word] = ident_code
    ident_code += 1

    return ident_code - 1


def add_to_const_table(num):
    global const_code
    const_table[num] = const_code
    const_code += 1

    return const_code - 1


def add_to_key_words_table(word):
    global key_word_code
    key_words_table[word] = key_word_code
    key_word_code += 1

    return key_word_code - 1


def tables_to_file():
    pass
