from lexer import Token, scan
from lyst import Lyst


"""
lyst -> head items
head -> key p_keys opt_keys
p_keys -> indent key p_keys | e
opt_keys -> indent :key opt_keys | e
items -> item items | e
item -> val p_vals opt_vals
p_vals -> indent val p_vals | e
opt_vals -> indent key::val opt_vals | e
key -> string
val -> string
"""

class Parser(object):
    def __init__(self, f):
        self.f     = f # fp
        self.peek  = scan(f)
        self.look  = None        
        self._lyst = None

    def move(self):
        self.look = self.peek
        self.peek = scan(self.f)

    def match(self, token):
        self.move()
        if self.look[0] != token:
            raise Exception('Expected token %s, got %s' % (token, self.look[0]))

    # lyst -> head items
    def lyst(self):
        p_keys, opt_keys = self.head()
        print p_keys
        print opt_keys
        self._lyst = Lyst(p_keys, opt_keys)
        # self.items()

    # head -> key p_keys opt_keys
    def head(self):
        key = self.key()
        self.move()
        p_keys = self.p_keys()
        opt_keys = self.opt_keys()
        return [key] + p_keys, opt_keys

    # p_keys -> indent key p_keys | e
    def p_keys(self):
        keys = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.String:
            keys.append(self.key())
            self.move()
        return keys

    # opt_keys -> indent :key opt_keys | e
    def opt_keys(self):
        keys = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.Colon:
            self.move()
            keys.append(self.key())
            self.move()
        return keys

    # key -> string
    def key(self):
        self.match(Token.String)
        return self.look[1]

with open('test.list', 'U') as f:
    p = Parser(f)
    p.lyst()
