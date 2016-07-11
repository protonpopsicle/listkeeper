from lexer import Token, scan, state
from lyst import Lyst


class ParseError(Exception):
    def __init__(self, message):
        msg = "line %s '%s'\n%s: %s" % (state['ln'], state['line_buffer'], self.__class__.__name__, message)
        super(ParseError, self).__init__(msg)

"""
lyst     -> head items
head     -> key p_keys opt_keys
p_keys   -> indent key p_keys | e
opt_keys -> indent :key opt_keys | e
items    -> item items | e
item     -> val p_vals opt_vals
p_vals   -> indent val p_vals | e
opt_vals -> indent key::val opt_vals | e
key      -> string
val      -> string
"""
class Parser(object):
    def __init__(self, f):
        self.f = f # fp
        self.peek = scan(f)
        print self.peek
        self.peek2 = scan(f)
        print self.peek2
        self.look = None
        self._lyst = None

    def move(self):
        self.look = self.peek
        self.peek = self.peek2
        self.peek2 = scan(self.f)
        print self.peek2

    def match(self, token):
        self.move()
        if self.look[0] != token:
            raise ParseError('expected token %s, got %s' % (token, self.look[0]))

    # lyst -> head items
    def lyst(self):
        p_keys, opt_keys = self.head()
        self._lyst = Lyst(p_keys, opt_keys)
        self.items()

    # head -> key p_keys opt_keys
    def head(self):
        self.move()
        key = self.key()
        self.move()
        p_keys = self.p_keys()
        opt_keys = self.opt_keys()
        return [key] + p_keys, opt_keys

    # p_keys -> indent key p_keys | e
    def p_keys(self):
        keys = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.String:
            self.move()
            keys.append(self.key())
            self.move()
        return keys

    # opt_keys -> indent :key opt_keys | e
    def opt_keys(self):
        keys = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.Colon:
            self.move()
            self.move()
            keys.append(self.key())
            self.move()
        return keys

    # items -> item items | e
    def items(self):
        while self.look[0] != Token.EOF:
            self.item()
        self._lyst.dump()

    # item -> val p_vals opt_vals
    def item(self):
        val = self.val()
        self.move()
        p_vals = [val] + self.p_vals()
        opt_vals = self.opt_vals()
        self._lyst.add_item(p_vals, opt_vals)

    # p_vals -> indent val p_vals | e
    def p_vals(self):
        vals = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.String and \
              self.peek2[0] != Token.Colon:
            self.move()
            vals.append(self.val())
            self.move()
        return vals

    # opt_vals -> indent key::val opt_vals | e
    def opt_vals(self):
        vals = []
        while self.look[0] == Token.Indent and self.peek[0] == Token.String and \
              self.peek2[0] == Token.Colon:
            self.move()
            key = self.key()
            self.match(Token.Colon)
            self.match(Token.Colon)
            self.move()
            vals.append((key, self.val()))
            self.move()
        return vals

    # key -> string
    def key(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise ParseError('expected %s, got %s' % (Token.String, self.look[0]))

    # val -> string
    def val(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise ParseError('expected %s, got %s' % (Token.String, self.look[0]))

with open('test.list', 'U') as f:
    p = Parser(f)
    try:
        p.lyst()
    except ParseError as e:
        print e.message
