import lexer
import parser

inp_file = 'tests_parser/test_incorrect_3.txt'
outp_file = 'lexems.txt'
atm_file = 'ATM_table.txt'
err_file = 'error_messages.txt'


scanning_result = lexer.scan(inp_file, outp_file)
if scanning_result:
    parser.parse(outp_file, atm_file, err_file)
