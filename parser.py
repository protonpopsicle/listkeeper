from lexer import Token, scan

def do_parse(f):
    while True:
        tok = scan(f)
        if not tok:
            break
        print tok

with open('test.list', 'U') as f:
    do_parse(f)

"""
header -> var vars kvars blankline
vars   -> var vars | e
kvars  -> kvar kvars | e
kvar   -> : var
var    -> string
"""
