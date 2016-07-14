import argparse
import csv
import sys

from parser import Parser, ParseError
from lexer import Lexer
from lyst import ValidationError


parser = argparse.ArgumentParser(description='Lyst command-line interface')
parser.add_argument('fname', type=str, help='path to a lyst file')
parser.add_argument('-s', '--sort', type=str, help='comma-separated field list')
parser.add_argument('-r', '--reverse', action='store_true', help='reverse sorting', default=False)

args = parser.parse_args()

#validate
sort_args = args.sort.split(',')

with open(args.fname, 'U') as f:
    lexer = Lexer(f)
    p = Parser(lexer)
    try:
        p.lyst()
    except ParseError as e:
        print 'ParserError: line %u: %s' % (lexer.ln, e.message)
    except ValidationError as e:
        print 'ValidationError: %s' % e.message
    
    writer = csv.DictWriter(sys.stdout, fieldnames=p._lyst.p_keys + p._lyst.opt_keys)
    writer.writeheader()
    for item in p._lyst.sort(*sort_args):
        writer.writerow(item)
