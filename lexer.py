ln = 1
cn = 0

class Token:
    String = 'str'
    Colon  = ':'
    Indent = 'indent'
    EOF    = 'EOF'

def peek(f, length=1):
    pos = f.tell()
    data = f.read(length)
    f.seek(pos)
    return data

def scan(f):
    global ln
    global cn
    char_buffer = ""
    while True:
        c = f.read(1)
        if not c:
            if len(char_buffer):
                return Token.String, char_buffer
            return Token.EOF, None
        cn += 1

        if c == '\n':
            ln += 1
            cn = 0
            char_buffer = ""
            if peek(f).isspace():
                return Token.Indent, None
        if c == ':':
            char_buffer = ""
            return Token.Colon, None
        else:
            if char_buffer or not c.isspace():
                char_buffer += c

        if peek(f) == '\n':
            if len(char_buffer):
                return Token.String, char_buffer
        elif peek(f) == ':':
            if len(char_buffer):
                return Token.String, char_buffer
