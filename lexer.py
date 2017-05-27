import utils
import tables


def scan(inp_filename, outp_filename):
    inp_file = open(inp_filename, 'r')
    outp_file = open(outp_filename, 'w')
    scanning_result = True

    ch = inp_file.read(1)
    line = 1
    column = 1
    if not ch:
        print('File is empty')
        scanning_result = False

    while ch:
        buf = ''
        lex_code = 0
        suppress_output = False

        if utils.is_whitespace(ch):
            while True:
                if ch == '\n':
                    line += 1
                    column = 0
                ch = inp_file.read(1)
                column += 1
                if (not ch) or (not utils.is_whitespace(ch)):
                    break
            suppress_output = True
        elif utils.is_digit(ch):
            outp_file.write(str(line) + ' ' + str(column) + ' ')
            while True:
                buf += ch
                ch = inp_file.read(1)
                column += 1
                if (not ch) or (not utils.is_digit(ch)):
                    break
            if not tables.in_const_table(buf):
                tables.add_to_const_table(buf)
            lex_code = tables.const_table[buf]
        elif utils.is_letter(ch):
            outp_file.write(str(line) + ' ' + str(column) + ' ')
            while True:
                buf += ch
                ch = inp_file.read(1)
                column += 1
                if (not ch) or (not (utils.is_digit(ch) or utils.is_letter(ch))):
                    break
            if tables.in_key_words_table(buf):
                lex_code = tables.key_words_table[buf]
            else:
                if not tables.in_ident_table(buf):
                    tables.add_to_ident_table(buf)
                lex_code = tables.ident_table[buf]
        elif utils.is_delimiter(ch):
            outp_file.write(str(line) + ' ' + str(column) + ' ')
            lex_code = ord(ch)
            ch = inp_file.read(1)
            column += 1
        elif ch == '(':
            ch = inp_file.read(1)
            column += 1
            if (not ch) or (ch != '*'):
                lex_code = ord('(')
            elif ch == '*':
                while True:
                    ch = inp_file.read(1)
                    column += 1
                    if (not ch):
                        print('line %d, column %d *) expected but end of the file found' % (line, column))
                        scanning_result = False
                        break
                    if (ch == '*'):
                        ch = inp_file.read(1)
                        column += 1
                        if ch and (ch == ')'):
                            suppress_output = True
                            ch = inp_file.read(1)
                            column += 1
                            break
                        elif not ch:
                            print('line %d, column %d *) expected but end of the file found' % (line, column))
                            scanning_result = False
        else:
            print('Invalid character: line %d column %d' % (line, column))
            scanning_result = False
            suppress_output = True
            ch = inp_file.read(1)
            column += 1
        if not suppress_output:
            outp_file.write(str(lex_code) + '\n')

    # test
    print(tables.ident_table)
    print(tables.const_table)
    print(tables.key_words_table)

    inp_file.close()
    outp_file.close()

    return scanning_result





