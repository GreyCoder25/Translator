import math


def code(root, names):
    if root is None:
        return
    if root.type == 'non-terminal':
        if root.text in {'<identifier>', '<procedure-identifier', '<function-identifier>',
                         '<unsigned-integer>', '<signal-program>', '<declarations>',
                         '<statements-list>'}:
            return code(root.descendants[0], names)
        elif root.text == '<function-characteristic>':
            return (int(code(root.descendants[1], names)), int(code(root.descendants[3], names)))
        elif root.text == '<program>':
            return code(root.descendants[3], names)
        elif root.text == '<block>':
            gen_code = ''
            for descendant in root.descendants:
                gen_code += code(descendant, names)
            return gen_code
        elif root.text == '<math-function-declaration>':
            if root.descendants[0].text == '<empty>':
                return code(root.descendants[0], names)
            else:
                return ('data\t\tSEGMENT\n' + code(root.descendants[1], names) +
                       '\ndata\t\tENDS\n\n')
        elif root.text == '<function-list>':
            if root.descendants[0].text == '<empty>':
                return code(root.descendants[0], names)
            else:
                return code(root.descendants[0], names) + code(root.descendants[1], names)
        elif root.text == '<function>':
            func_name = code(root.descendants[0], names)
            if not func_name in names:
                names.add(func_name)
                range_start = 0
                range_finish, num_points = code(root.descendants[3], names)
                step = (range_finish - range_start) / (num_points - 1)
                gen_code = ' ' + func_name + '\tdd\t'

                i = range_start
                gen_code += ('%.2f' % math.sin(i))
                i += step
                while i <= range_finish:
                    gen_code += ', ' + ('%.2f' % math.sin(i))
                    i += step
                gen_code += '\n'
                return gen_code
            else:
                print("Error while code generating: repeated name '%s'" % func_name)
                return ''

    elif root.type == 'terminal':
        if root.text == 'BEGIN':
            return ('code\t\tSEGMENT\n\t\t\tASSUME:\tcs:code, ds:data\nbegin:\n')
        elif root.text == 'END':
            return '\t\tmov\tax, 4c00h\n\t\tint\t21h\ncode\tENDS\n\t\tend\tbegin'
        elif root.text == '<empty>':
            return ''
        else:
            return root.text


def generate_code(code_tree, code_file):
    names = set([])
    with open(code_file, 'w') as f:
        f.write(code(code_tree.root, names))