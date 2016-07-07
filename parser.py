from lexer import Token, scan


"""
alist  -> head items
head   -> key keys
keys   -> indent key | indent :key | e
key    -> string

items  -> item items | e
item   -> value values
values -> indent value | indent key::value | e
value  -> string
"""
class Parser(object):
    def __init__(self, f, *args, **kwargs):
        self.f    = f # fp
        self.look = None
        self.parsed_keys     = []
        self.parsed_posikeys = []
        self.data = [[]] # contains lists of tuples
        super(Parser, self).__init__(*args, **kwargs)

    def move(self):
        self.look = scan(self.f)

    def match(self, tok):
        self.move()
        if self.look[0] != tok:
            raise Exception('Expected %s, got %s' % (tok, self.look[0]))

    # alist -> head items
    def alist(self):
        self.head()
        self.items()
        print self.data

    # head -> key keys
    def head(self):
        self.move()
        self.parsed_keys.append(self.key()) # first key
        self.keys()

    # keys -> indent key | indent :key | e
    def keys(self):
        self.move()
        while self.look[0] == Token.Indent:
            self.move()
            if self.look[0] == Token.Colon:
                self.move()
                self.parsed_keys.append(self.key())
            else:
                self.parsed_posikeys.append(self.key())
            self.move()

    # key -> string
    def key(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string')


    # items -> item items | e
    def items(self):
        while True:
            item = self.item()
            if not item:
                break
    
    # item -> value values
    def item(self):
        self.data.append([(self.parsed_keys[0], self.value())])
        self.values()
    
    # values -> indent value | indent key::value | e
    def values(self):
        self.move()
        pos = 0

        while self.look[0] == Token.Indent:
            self.move()
            lhs = self.value()
            self.move()

            if self.look[0] == Token.Colon:
                self.match(Token.Colon)
                self.move()
                if lhs not in self.parsed_keys:
                    raise Exception('No such key "%s".' % lhs)
                rhs = self.value()
                self.data[-1].append((lhs, rhs))
            else:
                if len(self.parsed_posikeys) > pos:
                    self.data[-1].append((self.parsed_posikeys[pos], lhs))
                else:
                    raise Exception('Extra positional value in item.')

            pos += 1
    
    # value -> string
    def value(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string, got %s' % self.look[0])

with open('test.list', 'U') as f:
    p = Parser(f)
    p.alist()
