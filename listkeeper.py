#! /usr/bin/env python
import argparse
import sys


class Catalog(object):
    def __init__(self, records, *args, **kwargs):
        self.cols = records[0]

        def get(record, i):
            if i < len(record):
                return record[i]
            return None

        self.records = [{h: get(record, i) for i, h in enumerate(self.cols)}
                        for record in records[1:]]

        super(Catalog, self).__init__(*args, **kwargs)

    def sort(self, col_name=None):
        if not col_name:
            col_name = self.cols[0]

        def keyfunc(record):
            x = record[col_name]
            if x:
                return x.lower()
            return ''

        return sorted(self.records, key=keyfunc)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    def read_record(f):
        record = []
        for line in f:
            x = line.strip()
            if x == '_':
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
        print 'found no records. exiting'
        return

    catalog = Catalog(records)
    for record in catalog.sort('title'):
        print record['title']
        if record['author(s)']:
            print '  ' + record['author(s)']
        if record['date']:
            print '  ' + record['date']

if __name__ == '__main__':
    main()
