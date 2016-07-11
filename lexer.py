state = dict(
    ln=1,
    line_buffer="")

class Token:
    String = 'String'
    Colon  = ':'
    Indent = 'Indent'
    EOF    = 'EOF'

def peek(f, length=1):
    pos = f.tell()
    data = f.read(length)
    f.seek(pos)
    return data

def scan(f):
    char_buffer = ""
    while True:
        c = f.read(1)
        if not c:
            if len(char_buffer):
                return Token.String, char_buffer.rstrip()
            return Token.EOF, None
        state['line_buffer'] += c

        # print state['line_buffer']

        if c == '\n':
            state['ln'] += 1
            state['line_buffer'] = ""
            char_buffer = ""
            continue
        elif len(char_buffer) or not c.isspace():
            if c == ':' and (not len(char_buffer) or peek(f) == ':'):
                return Token.Colon, None
            char_buffer += c

            peek2 = peek(f, 2)
            if peek2 == '::' or peek2[0] == '\n':
                return Token.String, char_buffer.rstrip()
        elif not peek(f).isspace():
            return Token.Indent, None


