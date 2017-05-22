import tables
from parse_tree import *

def parse(lex_file, atm_file, err_file):

    def lex_code(lexem):
        if tables.in_key_words_table(lexem):
            return tables.key_words_table[lexem]
        elif lexem == '1000':
            return 1000
        elif lexem == '500':
            return 500
        return ord(lexem)

    def corresponds(code1, code2):
        if code1 == 500 or code1 == 1000:
            return code1 == code2 - (code2 % 100)
        return code1 == code2

    parse_result = True
    lex_codes = []
    lex_lines = []
    lex_columns = []
    with open(lex_file) as f:
        for lex_info in f:
            lex_info = lex_info.rstrip().split(' ')
            if len(lex_info) != 1:
                lex_lines.append(lex_info[0])
                lex_columns.append(lex_info[1])
                lex_codes.append(lex_info[2])

    addresses = {}
    rule_numbers = {}
    ATM_table = []
    with open(atm_file) as f:
        index = 0
        rule_number = 1
        for line in f:
            rec = line.rstrip().split(' ')
            if rec[0] != '':
                addresses[rec[0]] = index
                rule_numbers[rec[0]] = rule_number
                rule_number += 1
            ATM_table.append(rec)
            index += 1

    error_messages = []
    with open(err_file) as f:
        for message in f:
            error_messages.append(message)

    ADDR = 0
    OP_CODE = 1
    AT = 2
    AF = 3

    line = addresses['START']
    col = OP_CODE
    call_stack = []

    lex_index = 0
    code_tree = ParseTree()
    error_flag = False
    error_message_flag = True
    error_code = 0
    while True:
        if col == OP_CODE:
            if ATM_table[line][col] in addresses:
                code_tree.add(ATM_table[line][col], 'non-terminal')
            else:
                if ATM_table[line][col] == '500' and corresponds(500, int(lex_codes[lex_index])):
                    code_tree.add(tables.const_decode_table[int(lex_codes[lex_index])], 'terminal')
                elif ATM_table[line][col] == '1000' and corresponds(1000, int(lex_codes[lex_index])):
                    code_tree.add(tables.ident_decode_table[int(lex_codes[lex_index])], 'terminal')
                else:
                    code_tree.add(ATM_table[line][col], 'terminal')

            if ATM_table[line][col] in addresses:
                call_stack.append(line)
                line = addresses[ATM_table[line][col]]
                if ATM_table[line][AF] == 'N' or ATM_table[line][AF][0] == '+':
                    error_message_flag = False
            else:
                if ATM_table[line][col] == '<empty>':
                    col = AF
                elif (ATM_table[line][col] == '#' or
                corresponds(lex_code(ATM_table[line][col]), int(lex_codes[lex_index]))):
                    lex_index += 1
                    col = AT
                else:
                    col = AF
        elif col == AT:
            if ATM_table[line][col] == 'N':
                line += 1
                col = OP_CODE
                code_tree.level_up()
            elif ATM_table[line][col] == 'T':
                line = call_stack.pop()
                code_tree.level_up()
                if not error_message_flag:
                    error_message_flag = True
            elif ATM_table[line][col] == 'OK':
                print('Parsing completed successfully')
                break
        elif col == AF:
            if ATM_table[line][col] =='N':
                line += 1
                col = OP_CODE
                code_tree.delete_last()
            elif ATM_table[line][col][0] == '+':
                line += int(ATM_table[line][col][1:])
                col = OP_CODE
                code_tree.delete_last()
            elif ATM_table[line][col] == 'T':
                line = call_stack.pop()
                if not error_flag:
                    col = AT
                else:
                    col = AF
                code_tree.level_up()
            elif ATM_table[line][col] == 'ERROR':
                print("Parsing didn't complete successfully, errors found")
                break
            else:
                if ATM_table[line][OP_CODE] not in addresses and error_message_flag:
                    print_error_message(lex_lines[lex_index], lex_columns[lex_index],
                    ATM_table[line][OP_CODE], error_messages)
                    parse_result = False
                if ATM_table[line][col] == 'F+':
                    error_flag = True
                if not error_message_flag:
                    error_message_flag = True

                line = call_stack.pop()
                code_tree.delete_last()

    # code_tree.print()
    return (parse_result, code_tree)

def print_error_message(line, column, lexem, err_list):
    err_code = 0
    if lexem == 'PROGRAM':
        err_code = 1
    elif lexem == ';':
        err_code = 2
    elif lexem == '.':
        err_code = 3
    elif lexem == 'DEFFUNC':
        err_code = 4
    elif lexem == 'SIN':
        err_code = 5
    elif lexem == '=':
        err_code = 6
    elif lexem == '\\':
        err_code = 7
    elif lexem == ',':
        err_code = 8
    elif lexem == '1000':
        err_code = 9
    elif lexem == '500':
        err_code = 10
    elif lexem == 'BEGIN':
        err_code = 11
    elif lexem == 'END':
        err_code = 12

    if err_code != 0:
        print('Line %s, column %s, error %s' % (line, column, err_list[err_code - 1]))