import argparse
import sys

from parser import Parser, ParseError
from lexer import Lexer
from lyst import ValidationError


def forgiving_itemgetter(*items):
    def g(obj):
        return tuple(obj.get(item, None) for item in items)
    return g

def do_query(items, query, key=None):
    if key:
        return [x for x in items if query.lower() in x.get(key, '').lower()]
    return [x for x in items if True in
            [query.lower() in v.lower() for v in x.values()]]

def error_out(msg, prefix='error'):
    print "%s: %s" % (prefix, msg)
    sys.exit(1)

def run(path, query, sort_keys, reverse, exclude_keys):
    with open(path, 'U') as f:
        lexer = Lexer(f)
        p = Parser(lexer)
        try:
            p.lyst()
        except ParseError as e:
            error_out('bad syntax: line %u: %s' % (lexer.ln, e.message))
        except ValidationError as e:
            error_out('invalid list: %s' % e.message)

    keys = p._lyst.p_keys + p._lyst.opt_keys
    q_key = None

    if query and '::' in query:
        q_key, query = query.split('::')[:2]
        if q_key not in keys:
            error_out('field \'%s\' not in [%s]' % (q_key, '|'.join(keys)), 'query error')

    for key in sort_keys:
        if key not in keys:
            error_out('field \'%s\' not in [%s]' % (key, '|'.join(keys)), 'sort error')

    if exclude_keys:
        for key in exclude_keys:
            if key not in keys:
                error_out('cannot exclude \'%s\'. no such field in [%s]' % (key, '|'.join(keys)))
        keys = [k for k in keys if k not in exclude_keys]

    print '|'.join(keys)

    items = p._lyst.items
    if query:
        items = do_query(items, query, q_key)

    if len(sort_keys):
        items = sorted(items, key=forgiving_itemgetter(*sort_keys), reverse=reverse)

    for item in items:
        row = []
        for k in keys:
            row.append(item.get(k, ''))
        print '|'.join(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ListKeeper command-line interface')
    parser.add_argument('path', type=str, help='path to a list file')
    parser.add_argument('-q', '--query', type=str,
                        help='search string or query of the form: <field>::<query>')
    parser.add_argument('-s', '--sort', type=str, help='comma-separated list of fields to sort by')
    parser.add_argument('-r', '--reverse', action='store_true', default=False,
                        help='reverse sorting')
    parser.add_argument('-x', '--exclude', type=str,
                        help='comma-separated list of fields to exclude from output')

    args = parser.parse_args()
    sort_keys    = []
    exclude_keys = []
    if args.sort:
        sort_keys = args.sort.split(',')
    if args.exclude:
        exclude_keys = args.exclude.split(',')

    run(args.path, args.query, sort_keys, args.reverse, exclude_keys)
