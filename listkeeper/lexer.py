class Token:
    String = 'String'
    Colon  = ':'
    SuperColon  = '::'
    Indent = 'Indent'
    EOF = 'EOF'

def get(list, i):
    try:
        return list[i]
    except IndexError:
        return None

class Lexer(object):
    def __init__(self, f):
        self.f = f
        self.tokens = []
        self.line = ''
        self.ln = 0

    def scan(self):
        # returns one token at a time
        if len(self.tokens):
           return self.tokens.pop(0)
        try:
            self.line = next(self.f).rstrip()
            self.ln += 1
            self.tokens += self.scan_line(self.line)
            return self.scan()
        except StopIteration:
            return Token.EOF, None

    def scan_line(self, line):
        # fills token buffer
        tokens = []
        if len(line):
            if line[0].isspace():
                tokens.append((Token.Indent, None))
                line = line.lstrip()

            char_buffer = ""
            for i, c in enumerate(line):
                if c == ':':
                    if get(line, i+1) == ':':
                        if len(char_buffer):
                            tokens.append((Token.String, char_buffer))
                            char_buffer = ""
                        tokens.append((Token.SuperColon, None))
                    elif i == 0:
                        tokens.append((Token.Colon, None))
                else:
                    char_buffer += c

            if len(char_buffer):
                tokens.append((Token.String, char_buffer))
        return tokens
