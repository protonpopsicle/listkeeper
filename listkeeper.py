#! /usr/bin/env python
import argparse
import sys

from listkeeper import parse, print_as_text, print_as_html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file')
    parser.add_argument('--format', help='output format',
                        choices=['text', 'html'], default='text')
    parser.add_argument('--col-width', help='output column character width',
                        type=int, default=36)
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
                break
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

    fields, parsed_recs = parse(records)

    if args.format == 'text':
        if sys.stdout.isatty():
            print print_as_text(parsed_recs, fields, col_width=args.col_width,
                                tty=True)
        else: # you're being piped or redirected
            print print_as_text(parsed_recs, fields, col_width=args.col_width)
    elif args.format == 'html':
        print 'html'
        # print render_html(catalog)

if __name__ == '__main__':
    main()
