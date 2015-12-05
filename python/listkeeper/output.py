from datetime import datetime


class ANSI:
    END = '\033[0m'
    BOLD = '\033[1m'

def print_as_text(records, fields, tty=None, col_width=None):
    def render_header(col, do_ansi=False):
        name = fields[col][0]
        return ' ' + name.upper() + ' '

    def render_item(record, col, do_ansi=False):
        field = fields[col]
        item = record[col]
        if item == None:
            return ''

        _type = field[1]
        if _type == list:
            o = ', '.join(item)
        elif _type == datetime:
            o = item.strftime('%d, %b %Y')
        else:
            o = str(item)
        if col_width and len(o) > col_width:
            o = o[:col_width].strip() + '...'

        if tty and do_ansi:
            if col == 0:
                o = ANSI.BOLD + o + ANSI.END
        return ' ' + o + ' '

    column_widths = []
    for i, field in enumerate(fields):
        rendered_items = [render_item(r, i) for r in records]
        max_w = max([len(r) for r in [render_header(i)] + rendered_items])
        column_widths.append(max_w)

    out = ''
    for i, field in enumerate(fields):
        w = column_widths[i]
        h = render_header(i)
        out += ('{: <%s}' % w).format(h)
    out += '\n'

    for i, field in enumerate(fields):
        w = column_widths[i]
        out += ('{: <%s}' % w).format(' ---')
    out += '\n'

    for rec in records:
        for i, field in enumerate(fields):
            w = column_widths[i]
            item = render_item(rec, i)
            out += ('{: <%s}' % w).format(item)
        out += '\n'

    for i, field in enumerate(fields):
        w = column_widths[i]
        out += ('{:->%s}' % w).format('|')
    return out

def print_as_html(header, records):
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
