from getch import getche
import click
import pprint
import ox

lexer = ox.make_lexer([
    ('COMMENT', r';(.)*'),
    ('NEW_LINE', r'\n+'),
    ('OPEN_BRACKET', r'\('),
    ('CLOSE_BRACKET', r'\)'),
    ('NAME', r'[a-zA-Z_][a-zA-Z_0-9-]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
])

token_list = [
    'NAME',
    'NUMBER',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
]

parser = ox.make_parser([

    ('tuple : OPEN_BRACKET term CLOSE_BRACKET', lambda openbracket, term, closebracket: term),
    ('tuple : OPEN_BRACKET CLOSE_BRACKET', lambda open_bracket, close_bracket: '()'),
    ('term : atom term', lambda term, other_term: (term, other_term)),
    ('term : atom', lambda term: term),
    ('atom : tuple', lambda op: (op)),
    ('atom : NAME', lambda name: name),
    ('atom : NUMBER', lambda x: int(x)),

], token_list)

data = [0]
ptr = 0
code_ptr = 0
breakpoints = []

@click.command()
@click.argument('source_file',type=click.File('r'))
def build(source_file):

    print_ast = pprint.PrettyPrinter(width=60, compact=True)
    source = source_file.read()

    tokens = lexer(source)
    # print('tokens:')
    # print(tokens)

    tokens = [value for value in tokens if str(value)[:7] != 'COMMENT' and str(value)[:8] != 'NEW_LINE']
    ast = parser(tokens)

    ast = ('do', ('add', '2'), 'right', ('add', '3'), 'left', ('loop', 'dec', 'right', 'inc', 'left'), 'right', ('add', '48'), 'print')

    # print_ast.pprint(ast)
    print(ast)
    lf(ast, code_ptr, ptr)


def lf(source, code_ptr, ptr):

    while code_ptr < len(source):
        command = source[code_ptr]

        if isinstance(command, tuple):

            if command[0] == 'add':
                data[ptr] = (data[ptr] + int(command[1])) % 256;
            elif command[0] == 'sub':
                data[ptr] = (data[ptr] - int(command[1])) % 256;
            elif command[0] == 'do-after':
                ...
            elif command[0] == 'do-before':
                ...
            elif command[0] == 'loop':
                ...
        elif command == 'inc':
            data[ptr] = (data[ptr] + 1) % 256;
        elif command == 'dec':
            data[ptr] = (data[ptr] - 1) % 256;
        elif command == 'right':
            ptr += 1
            if ptr == len(data):
                data.append(0)
        elif command == 'left':
            ptr -= 1
        elif command == 'print':
            print(chr(data[ptr]), end='')
        elif command == 'read':
            data[ptr] = ord(getche())



        code_ptr += 1

if __name__ == '__main__':
    build()