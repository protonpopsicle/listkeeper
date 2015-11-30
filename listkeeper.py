#! /usr/bin/env python
import argparse
import sys

from datetime import datetime
from dateutil.parser import parse


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

def list_get(alist, i, default=None):
    try:
        return alist[i]
    except IndexError:
        return default

def parse_column(records, col):
    # check for explicit types
    name = records[0][col]
    parts = name.split('(s)')
    if len(parts) == 2:
        return parts[0], list

    # infer implicit types
    for record in records[1:]:
        item = list_get(record, col)
        if item: # don't count empty items
            if is_int(item):
                return name, int
            elif is_float(item):
                return name, float
            elif is_date(item):
                return name, datetime
            else:
                return name, str
    return name, type(None)

# def type_convert(col_def, records):
#     col_def
#     pass

class Catalog(object):
    def __init__(self, records, *args, **kwargs):
        self.columns = []
        for idx, val in enumerate(records[0]):
            self.columns.append(parse_column(records, idx))
        print self.columns

        self.records = []
        for record in records[1:]:
            self.records.append({
                h[0]: list_get(record, i, '') for i, h in enumerate(self.columns)})

        super(Catalog, self).__init__(*args, **kwargs)

    def sort(self, header=None):
        if not header:
            header = self.columns[0]

        return sorted(self.records, key=lambda r: r[header].lower())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file')
    parser.add_argument('--format', help='output format',
                        choices=['text', 'html'], default='text')
    args = parser.parse_args()

    def read_record(f):
        record = []
        for line in f:
            x = line.strip()
            if x == '.':
                record.append('')
            elif x:
                record.append(x)
            else:
                return record

    records = []

    with open(args.infile, 'r') as f:
        while True:
            record = read_record(f)
            if not record:
                break
            records.append(record)

    if not len(records):
        print 'file contains no records. exiting'
        return

    catalog = Catalog(records)

    def render_text(header, records):
        template = ''
        for h in header:
            max_len = max([len(r[h]) for r in records])
            template += '{%s:%s}' % (h, max_len + 3)

        out = ''
        for i, r in enumerate(records):
            out += '%s. %s\n' % (i + 1, template.format(**r))
        return out

    def render_html(header, records):
        document = '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>list-keeper</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container">
                    <table class="table table-striped table-condensed table-bordered">%s</table>
                </div>
            </body>
        </html>
        '''
        tmpl = '<tr>' + ''.join(['<td>{%s}</td>' % h for h in header]) + '</tr>'
        return document % ''.join([tmpl.format(**r) for r in records])

    if args.format == 'text':
        print render_text(catalog.header, catalog.sort())
    elif args.format == 'html':
        print render_html(catalog.header, catalog.sort())

if __name__ == '__main__':
    main()
