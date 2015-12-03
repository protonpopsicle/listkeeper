from datetime import datetime
from dateutil.parser import parse as parse_date


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
        parse_date(string)
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
                typed_rec.append([i.strip() for i in item.split(',')])
            elif _type in [int, float]:
                typed_rec.append(_type(item))
            elif _type == datetime:
                typed_rec.append(parse_date(item))
            else:
                typed_rec.append(item)
    return typed_rec

def parse(records):
    fields = []
    for i, x in enumerate(records[0]):
        fields += [infer_field(records, i)]

    parsed_recs = []
    for rec in records[1:]:
        parsed_recs += [parse_record(rec, fields)]
    return fields, parsed_recs
