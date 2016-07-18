import argparse
import sys

from parser import Parser, ParseError
from lexer import Lexer
from lyst import ValidationError


def do_it(fname, sort_args, reverse):
    with open(fname, 'U') as f:
        lexer = Lexer(f)
        p = Parser(lexer)
        try:
            p.lyst()
        except ParseError as e:
            print 'ParserError: line %u: %s' % (lexer.ln, e.message)
        except ValidationError as e:
            print 'ValidationError: %s' % e.message

        keys = p._lyst.p_keys + p._lyst.opt_keys
        print '|'.join(keys)
            
        for item in p._lyst.sort(*sort_args):
            row = []
            for k in keys:
                row.append(item.get(k, ''))
            print '|'.join(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lyst command-line interface')
    parser.add_argument('fname', type=str, help='path to a lyst file')
    parser.add_argument('-s', '--sort', type=str, help='comma-separated field list')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse sorting', default=False)

    args = parser.parse_args()

    #validate
    sort_args = args.sort.split(',')
    do_it(args.fname, sort_args, args.reverse)

