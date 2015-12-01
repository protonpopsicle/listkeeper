#! /usr/bin/env python
import argparse
import sys

from datetime import datetime
from dateutil.parser import parse


class ANSI:
    END = '\033[0m'
    BOLD = '\033[1m'
    # RED = '\e[31m'
    # YELLOW = '\e[33m'
    # UNDERLINE = '\e[4m'

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

def infer_field(records, i):
    # check for explicit types
    name = records[0][i]
    parts = name.split('(s)')
    if len(parts) == 2:
        return parts[0], list

    # infer implicit types
    for record in records[1:]:
        item = list_get(record, i)
        if item:
            if is_int(item):
                return name, int
            elif is_float(item):
                return name, float
            elif is_date(item):
                return name, datetime
    return name, str

def parse_record(rec, fields):
    typed_rec = []
    for i, field in enumerate(fields):
        name, _type = field
        item = list_get(rec, i)
        if not item:
            if _type == list:
                typed_rec.append([])
            else:
                typed_rec.append(None)
        else:
            if _type == list:
                typed_rec.append(item.split(','))
            elif _type in [int, float]:
                typed_rec.append(_type(item))
            elif _type == datetime:
                typed_rec.append(parse(item))
            else:
                typed_rec.append(item)
    return typed_rec

    # def sort(self, header=None):
    #     if not header:
    #         header = self.columns[0]

    #     return sorted(self.records, key=lambda r: r[header].lower())


def render_as_text(records, fields, tty=None, maxlen=None):
    def render_item(record, col):
        field = fields[col]
        item = record[col]
        if item == None:
            return ''

        _type = field[1]
        if _type == list:
            o = ''.join(item)
        elif _type == datetime:
            o = item.strftime('%d, %b %Y')
        else:
            o = str(item)
        if maxlen and len(o) > maxlen:
            o = o[:maxlen] + '...'

        if tty and col == 0:
            return ANSI.BOLD + o + ANSI.END
        return o

    template = ''

    for i, field in enumerate(fields):
        rendered_items = [render_item(r, i) for r in records]
        widest = max([len(r) for r in rendered_items])
        template += '{%s: <%s}' % (i, widest + 3)

    out = ''
    for rec in records:
        rendered_items = [render_item(rec, i) \
                          for i, item in enumerate(fields)]
        out += '%s\n' % template.format(*rendered_items)
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
                record.append(None)
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
        print 'list contains no records. exiting'
        return

    fields = []
    for i, x in enumerate(records[0]):
        fields += [infer_field(records, i)]
    # print fields

    parsed_recs = []
    for rec in records[1:]:
        parsed_recs += [parse_record(rec, fields)]
    # print parsed_recs

    if args.format == 'text':
        if sys.stdout.isatty():
            print render_as_text(parsed_recs, fields, tty=True, maxlen=25)
        else: # you're being piped or redirected
            print render_as_text(parsed_recs, fields)
    elif args.format == 'html':
        print 'html'
        # print render_html(catalog)

if __name__ == '__main__':
    main()
