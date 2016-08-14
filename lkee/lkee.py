import argparse
import operator
import sys

from parser import Parser, ParseError
from lexer import Lexer
from lyst import ValidationError


def grep(items, query, key=None):
    if key:
        return [x for x in items if query.lower() in x[key].lower()]
    return [x for x in items if True in
            [query.lower() in v.lower() for v in x.values()]]

def sort(items, reverse=False, *args):
    key = operator.itemgetter(*args)
    return sorted(items, key=key, reverse=reverse)

def run(fname, query, sort_args, reverse):
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
        query_key = None

        # validate query
        if query and '::' in query:
            parts = query.split('::')
            if parts[0] not in keys:
                raise Exception('no such key: "%s"' % key)
            if len(parts) < 2:
                raise Exception('malformed query: "%s"' % query)
            query_key, query = parts[:2]

        # validate sort_args
        for key in sort_args:
            if key not in keys:
                raise Exception('no such key: "%s"' % key)

        print '|'.join(keys)

        items = p._lyst.items
        if query:
            items = grep(items, query, query_key)

        if len(sort_args):
            items = sort(items, reverse, *sort_args)

        for item in items:
            row = []
            for k in keys:
                row.append(item.get(k, ''))
            print '|'.join(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='ListKeeper command-line interface')
    parser.add_argument('fname', type=str, help='path to a lyst file')
    parser.add_argument('-s', '--sort', type=str,
                        help='comma-separated field list')
    parser.add_argument('-g', '--grep', type=str,
                        help='search string or query <key>::<query>')
    parser.add_argument('-r', '--reverse', action='store_true', default=False,
                        help='reverse sorting')

    args = parser.parse_args()
    sort_args = []
    if args.sort:
        sort_args = args.sort.split(',')

    run(args.fname, args.grep, sort_args, args.reverse)
