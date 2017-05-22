import lexer
import parser
import code_generator

inp_file = 'tests_parser/test_incorrect_3.txt'
lex_file = 'lexems.txt'
atm_file = 'ATM_table.txt'
err_file = 'error_messages.txt'
output_code_file = 'asm_code.txt'


scanning_result = lexer.scan(inp_file, lex_file)
if scanning_result:
    parse_result = parser.parse(lex_file, atm_file, err_file)
    if parse_result[0]:
        code_tree = parse_result[1]
        code_generator.generate_code(code_tree, output_code_file)
